import mysql.connector as mysql

conn = mysql.connect(
    host="192.168.122.11",
    user="havok",
    password="maria",
    database="apple_health"
)

if conn.is_connected():
    print("Connected to the database")
