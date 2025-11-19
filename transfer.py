#!/usr/bin/env python3
import argparse
import sys
from decimal import Decimal
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import errorcode

def parse_dt(dt_str):
    """
    Parse 'YYYY-MM-DD HH:MM:SS ±HHMM' into UTC naive 'YYYY-MM-DD HH:MM:SS'.
    Returns None if dt_str is falsy.
    """
    if not dt_str:
        return None
    # Example: "2024-06-29 15:00:12 +0530"
    aware = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S %z")
    utc_naive = aware.astimezone(timezone.utc).replace(tzinfo=None)
    return utc_naive.strftime("%Y-%m-%d %H:%M:%S")

def parse_date_only(d_str):
    """
    Parse 'YYYY-MM-DD' into date string, or return None.
    """
    if not d_str:
        return None
    return datetime.strptime(d_str, "%Y-%m-%d").date().isoformat()

def to_decimal(val):
    if val is None:
        return None
    try:
        return Decimal(val)
    except Exception:
        return None

def ensure_indexes(cnx):
    cur = cnx.cursor()
    # Unique index to support the ON DUPLICATE KEY UPDATE used by your trigger
    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS uq_health_sample
        ON health_sample (user_id, sample_type, start_time, end_time)
    """)
    cur.close()
    cnx.commit()

def insert_health_record(cur, user_id, attrib):
    sql = """
    INSERT INTO health_record
      (user_id, type, unit, value, source_name, source_version, device, creation_date, start_date, end_date)
    VALUES
      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    value = to_decimal(attrib.get('value'))
    data = (
        user_id,
        attrib.get('type'),
        attrib.get('unit'),
        value,
        attrib.get('sourceName'),
        attrib.get('sourceVersion'),
        attrib.get('device'),
        parse_dt(attrib.get('creationDate')),
        parse_dt(attrib.get('startDate')),
        parse_dt(attrib.get('endDate')),
    )
    cur.execute(sql, data)
    return cur.lastrowid

def insert_metadata_entries(cur, record_id, elem):
    meta_sql = "INSERT INTO metadata_entry (record_id, meta_key, meta_value) VALUES (%s, %s, %s)"
    for child in list(elem):
        if child.tag == 'MetadataEntry':
            cur.execute(meta_sql, (record_id, child.get('key'), child.get('value')))

def insert_workout(cur, user_id, attrib):
    sql = """
    INSERT INTO workout
      (user_id, activity_type, duration, duration_unit,
       total_distance, total_distance_unit, total_energy_burned, total_energy_burned_unit,
       start_date, end_date, source_name)
    VALUES
      (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        user_id,
        attrib.get('workoutActivityType'),
        to_decimal(attrib.get('duration')),
        attrib.get('durationUnit'),
        to_decimal(attrib.get('totalDistance')),
        attrib.get('totalDistanceUnit'),
        to_decimal(attrib.get('totalEnergyBurned')),
        attrib.get('totalEnergyBurnedUnit'),
        parse_dt(attrib.get('startDate')),
        parse_dt(attrib.get('endDate')),
        attrib.get('sourceName'),
    )
    cur.execute(sql, data)

def insert_activity_summary(cur, user_id, attrib):
    sql = """
    INSERT INTO activity_summary
      (user_id, date, active_energy_burned, move_time, exercise_time, stand_hours)
    VALUES
      (%s, %s, %s, %s, %s, %s)
    """
    data = (
        user_id,
        parse_date_only(attrib.get('dateComponents')),
        to_decimal(attrib.get('activeEnergyBurned')),
        int(attrib.get('appleMoveTime')) if attrib.get('appleMoveTime') else None,
        int(attrib.get('appleExerciseTime')) if attrib.get('appleExerciseTime') else None,
        int(attrib.get('appleStandHours')) if attrib.get('appleStandHours') else None,
    )
    cur.execute(sql, data)

def stream_import(xml_path, db_cfg, user_id, commit_every=500):
    try:
        cnx = mysql.connector.connect(**db_cfg)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid MySQL credentials", file=sys.stderr)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist", file=sys.stderr)
        else:
            print(str(err), file=sys.stderr)
        sys.exit(1)

    try:
        ensure_indexes(cnx)
        cur = cnx.cursor()
        batch = 0

        # Use iterparse to stream large XML files
        context = ET.iterparse(xml_path, events=("end",))
        for event, elem in context:
            tag = elem.tag

            if tag == 'Record':
                record_id = insert_health_record(cur, user_id, elem.attrib)
                insert_metadata_entries(cur, record_id, elem)
                batch += 1

            elif tag == 'Workout':
                insert_workout(cur, user_id, elem.attrib)
                batch += 1

            elif tag == 'ActivitySummary':
                insert_activity_summary(cur, user_id, elem.attrib)
                batch += 1

            if batch >= commit_every:
                cnx.commit()
                batch = 0

            # Free memory
            elem.clear()

        if batch > 0:
            cnx.commit()
        cur.close()
    finally:
        cnx.close()

def main():
    parser = argparse.ArgumentParser(description="Import Apple Health XML export into MariaDB")
    parser.add_argument("--xml", required=True, help="Path to export.xml")
    parser.add_argument("--user-id", type=int, required=True, help="Existing user_id to associate data with")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--db", required=True, help="Database name")
    parser.add_argument("--db-user", required=True, help="Database user")
    parser.add_argument("--db-pass", required=True, help="Database password")
    parser.add_argument("--commit-every", type=int, default=500, help="Commit interval for batch inserts")
    args = parser.parse_args()

    db_cfg = {
        "host": args.host,
        "port": args.port,
        "database": args.db,
        "user": args.db_user,
        "password": args.db_pass,
    }
    stream_import(args.xml, db_cfg, args.user_id, args.commit_every)
    print("Import completed successfully.")

if __name__ == "__main__":
    main()
