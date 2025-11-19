# api.py
import os
import shutil
import zipfile
import subprocess
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Any, Dict
from datetime import datetime, date
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import uvicorn
import hashlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and chat service
from database import pool, fetch_all, fetch_one, get_connection
from chat_service import ChatService

# Initialize chat service
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables")
    chat_service = None
else:
    chat_service = ChatService(GEMINI_API_KEY)

# Helpers
def as_sql_ts(dt: datetime) -> str:
    """
    Normalize incoming datetimes to UTC and return 'YYYY-MM-DD HH:MM:SS' for DATETIME columns.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

# Pydantic response models
class HRVDaily(BaseModel):
    day: date
    avg_sdnn_ms: Optional[float]

class HRDaily(BaseModel):
    day: date
    avg_bpm: Optional[float]
    min_bpm: Optional[float]
    max_bpm: Optional[float]
    unit: Optional[str]

class ActivitySummaryOut(BaseModel):
    date: date
    active_energy_burned: Optional[float]
    move_time: Optional[int]
    exercise_time: Optional[int]
    stand_hours: Optional[int]

class WorkoutOut(BaseModel):
    workout_id: int
    activity_type: str
    duration: Optional[float]
    duration_unit: Optional[str]
    total_distance: Optional[float]
    total_distance_unit: Optional[str]
    total_energy_burned: Optional[float]
    total_energy_burned_unit: Optional[str]
    start_date: datetime
    end_date: datetime
    source_name: Optional[str]


class MotionContextCount(BaseModel):
    motion_context: str
    count: int

class DateRange(BaseModel):
    start: datetime
    end: datetime

class OverviewOut(BaseModel):
    window_start: str
    window_end: str
    latest_hrv_ms: Optional[float]
    avg_hrv_7d_ms: Optional[float]
    latest_hr_avg_bpm: Optional[float]
    hr_min_bpm: Optional[float]
    hr_max_bpm: Optional[float]

class DailySnapshotOut(BaseModel):
    day: date
    snapshot: Dict[str, Any]

class ChatCreate(BaseModel):
    chat_name: Optional[str] = "Health Chat"

class ChatMessage(BaseModel):
    message: str
    use_health_data: bool = False
    insight_type: str = "raw_data"  # raw_data, trend_summary, consistency_score, correlations, comprehensive

class ChatRename(BaseModel):
    new_name: str

# FastAPI app
app = FastAPI(title="Health API", version="1.0.0")

# CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBasic()

# Upload directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Helper functions for auth
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username: str, password: str) -> Optional[int]:
    """Verify user credentials and return user_id if valid"""
    cnx = get_connection()
    try:
        cur = cnx.cursor(dictionary=True)
        cur.execute(
            "SELECT user_id, password FROM user WHERE username = %s",
            (username,)
        )
        result = cur.fetchone()
        cur.close()
        
        if result and result['password'] == hash_password(password):
            return result['user_id']
        return None
    finally:
        cnx.close()

def create_user(username: str, name: str, password: str) -> int:
    """Create a new user and return user_id"""
    cnx = get_connection()
    try:
        cur = cnx.cursor()
        cur.execute(
            "INSERT INTO user (username, name, password) VALUES (%s, %s, %s)",
            (username, name, hash_password(password))
        )
        user_id = cur.lastrowid
        cnx.commit()
        cur.close()
        return user_id
    finally:
        cnx.close()

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> int:
    """Dependency to get current authenticated user"""
    user_id = verify_user(credentials.username, credentials.password)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user_id

def require_valid_range(start: datetime, end: datetime):
    if end <= start:
        raise HTTPException(status_code=400, detail="end must be after start")

# Authentication endpoints
@app.post("/api/register")
async def register(username: str = Form(...), name: str = Form(...), password: str = Form(...)):
    """Register a new user"""
    try:
        # Check if user already exists
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            cur.execute("SELECT user_id FROM user WHERE username = %s", (username,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Username already exists")
            cur.close()
        finally:
            cnx.close()
        
        user_id = create_user(username, name, password)
        return {"success": True, "user_id": user_id, "message": "User created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/login")
async def login(username: str = Form(...), password: str = Form(...)):
    """Login endpoint"""
    user_id = verify_user(username, password)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "user_id": user_id}

@app.get("/api/me")
async def get_me(user_id: int = Depends(get_current_user)):
    """Get current user info"""
    cnx = get_connection()
    try:
        cur = cnx.cursor(dictionary=True)
        cur.execute("SELECT user_id, username, name FROM user WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        return user
    finally:
        cnx.close()

@app.delete("/api/user/delete")
async def delete_user(user_id: int = Depends(get_current_user)):
    """Delete current user and all associated data"""
    cnx = get_connection()
    try:
        cur = cnx.cursor()
        
        # Delete all user data (in order due to foreign key constraints)
        # Delete chat messages
        cur.execute("DELETE cm FROM chat_message cm JOIN chats c ON cm.chat_id = c.chat_id WHERE c.user_id = %s", (user_id,))
        
        # Delete chats
        cur.execute("DELETE FROM chats WHERE user_id = %s", (user_id,))
        
        # Delete metadata entries
        cur.execute("""
            DELETE me FROM metadata_entry me 
            JOIN health_record hr ON me.record_id = hr.record_id 
            WHERE hr.user_id = %s
        """, (user_id,))
        
        # Delete health records
        cur.execute("DELETE FROM health_record WHERE user_id = %s", (user_id,))
        
        # Delete health samples
        cur.execute("DELETE FROM health_sample WHERE user_id = %s", (user_id,))
        
        # Delete HRV data
        cur.execute("DELETE FROM hrv WHERE user_id = %s", (user_id,))
        
        # Delete activity summaries
        cur.execute("DELETE FROM activity_summary WHERE user_id = %s", (user_id,))
        
        # Delete workouts
        cur.execute("DELETE FROM workout WHERE user_id = %s", (user_id,))
        
        # Finally, delete the user
        cur.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
        
        cnx.commit()
        cur.close()
        
        return {"success": True, "message": "User account and all data deleted successfully"}
    except Exception as e:
        cnx.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    finally:
        cnx.close()

# Upload endpoint
@app.post("/api/upload")
async def upload_export(file: UploadFile = File(...), user_id: int = Depends(get_current_user)):
    """Upload and process Apple Health export zip file"""
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only ZIP files are allowed")
    
    # Create user-specific upload directory
    user_upload_dir = UPLOAD_DIR / str(user_id)
    user_upload_dir.mkdir(exist_ok=True)
    
    # Save uploaded file
    zip_path = user_upload_dir / file.filename
    try:
        with open(zip_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Extract zip file
        extract_dir = user_upload_dir / "extracted"
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_dir.mkdir()
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        # Look for export.xml in apple_health_export folder
        export_xml = extract_dir / "apple_health_export" / "export.xml"
        if not export_xml.exists():
            # Try direct export.xml
            export_xml = extract_dir / "export.xml"
            if not export_xml.exists():
                raise HTTPException(
                    status_code=400, 
                    detail="Could not find export.xml in apple_health_export folder"
                )
        
        # Run transfer.py to import data
        result = subprocess.run([
            "python3", "transfer.py",
            "--xml", str(export_xml),
            "--user-id", str(user_id),
            "--host", os.getenv("DB_HOST", "192.168.122.11"),
            "--port", os.getenv("DB_PORT", "3306"),
            "--db", os.getenv("DB_NAME", "apple_health"),
            "--db-user", os.getenv("DB_USER", "havok"),
            "--db-pass", os.getenv("DB_PASS", "maria"),
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            raise HTTPException(
                status_code=500,
                detail=f"Import failed: {result.stderr}"
            )
        
        # Cleanup
        shutil.rmtree(extract_dir)
        zip_path.unlink()
        
        return {
            "success": True,
            "message": "Health data imported successfully",
            "output": result.stdout
        }
        
    except zipfile.BadZipFile:
        raise HTTPException(status_code=400, detail="Invalid ZIP file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Protected endpoints - require authentication
@app.get("/api/users/{user_id}/hrv/daily", response_model=List[HRVDaily])
def hrv_daily(user_id: int,
              start: datetime = Query(..., description="ISO 8601 datetime, e.g., 2024-06-01T00:00:00Z"),
              end:   datetime = Query(..., description="ISO 8601 datetime, e.g., 2024-07-01T00:00:00Z"),
              current_user: int = Depends(get_current_user)):
    require_valid_range(start, end)
    s, e = as_sql_ts(start), as_sql_ts(end)
    sql = """
      SELECT DATE(start_date) AS day, AVG(value) AS avg_sdnn_ms
      FROM hrv
      WHERE user_id=%s AND start_date >= %s AND start_date < %s
      GROUP BY DATE(start_date)
      ORDER BY day
    """
    return fetch_all(sql, (user_id, s, e))

@app.get("/api/users/{user_id}/heart-rate/daily", response_model=List[HRDaily])
def heart_rate_daily(user_id: int,
                     start: datetime = Query(...),
                     end:   datetime = Query(...),
                     limit: int = Query(500, ge=1, le=5000),
                     offset: int = Query(0, ge=0),
                     current_user: int = Depends(get_current_user)):
    require_valid_range(start, end)
    s, e = as_sql_ts(start), as_sql_ts(end)
    sql = """
      SELECT DATE(start_time) AS day,
             AVG(avg_value)   AS avg_bpm,
             MIN(min_value)   AS min_bpm,
             MAX(max_value)   AS max_bpm,
             unit
      FROM health_sample
      WHERE user_id=%s
        AND sample_type='heart_rate'
        AND start_time >= %s AND end_time < %s
      GROUP BY DATE(start_time), unit
      ORDER BY day
      LIMIT %s OFFSET %s
    """
    return fetch_all(sql, (user_id, s, e, limit, offset))

@app.get("/api/users/{user_id}/activity/summary", response_model=List[ActivitySummaryOut])
def activity_summary(user_id: int,
                     start: datetime = Query(...),
                     end:   datetime = Query(...),
                     current_user: int = Depends(get_current_user)):
    require_valid_range(start, end)
    s, e = as_sql_ts(start), as_sql_ts(end)
    sql = """
      SELECT date, active_energy_burned, move_time, exercise_time, stand_hours
      FROM activity_summary
      WHERE user_id=%s AND date >= DATE(%s) AND date < DATE(%s)
      ORDER BY date
    """
    return fetch_all(sql, (user_id, s, e))

@app.get("/api/users/{user_id}/workouts", response_model=List[WorkoutOut])
def workouts(user_id: int,
             start: datetime = Query(...),
             end:   datetime = Query(...),
             limit: int = Query(200, ge=1, le=2000),
             offset: int = Query(0, ge=0),
             current_user: int = Depends(get_current_user)):
    require_valid_range(start, end)
    s, e = as_sql_ts(start), as_sql_ts(end)
    sql = """
      SELECT workout_id, activity_type, duration, duration_unit,
             total_distance, total_distance_unit, total_energy_burned, total_energy_burned_unit,
             start_date, end_date, source_name
      FROM workout
      WHERE user_id=%s AND start_date >= %s AND start_date < %s
      ORDER BY start_date
      LIMIT %s OFFSET %s
    """
    return fetch_all(sql, (user_id, s, e, limit, offset))

@app.get("/api/users/{user_id}/heart-rate/motion-context", response_model=List[MotionContextCount])
def motion_context_counts(user_id: int,
                          start: datetime = Query(...),
                          end:   datetime = Query(...),
                          current_user: int = Depends(get_current_user)):
    require_valid_range(start, end)
    s, e = as_sql_ts(start), as_sql_ts(end)
    sql = """
      SELECT me.meta_value AS motion_context, COUNT(*) AS count
      FROM metadata_entry me
      JOIN health_record hr ON hr.record_id = me.record_id
      WHERE hr.user_id=%s
        AND me.meta_key='HKMetadataKeyHeartRateMotionContext'
        AND hr.start_date >= %s AND hr.start_date < %s
      GROUP BY me.meta_value
      ORDER BY count DESC
    """
    return fetch_all(sql, (user_id, s, e))

# Optional GET overview with query params
@app.get("/api/users/{user_id}/overview", response_model=OverviewOut)
def overview_get(user_id: int,
                 start: datetime = Query(...),
                 end:   datetime = Query(...),
                 current_user: int = Depends(get_current_user)):
    require_valid_range(start, end)
    return _overview_common(user_id, start, end)

# POST overview with body params
@app.post("/api/users/{user_id}/overview", response_model=OverviewOut)
def overview_post(user_id: int, body: DateRange, current_user: int = Depends(get_current_user)):
    require_valid_range(body.start, body.end)
    return _overview_common(user_id, body.start, body.end)

@app.get("/api/users/{user_id}/daily-snapshot", response_model=List[DailySnapshotOut])
def daily_snapshot(user_id: int,
                   start: datetime = Query(...),
                   end: datetime = Query(...),
                   current_user: int = Depends(get_current_user)):
    """Get daily snapshots using fn_user_daily_snapshot stored function"""
    require_valid_range(start, end)
    
    # Generate list of dates between start and end
    start_date = start.date()
    end_date = end.date()
    
    results = []
    current_date = start_date
    
    cnx = get_connection()
    try:
        cur = cnx.cursor()
        while current_date < end_date:
            # Call the stored function
            cur.execute("SELECT fn_user_daily_snapshot(%s, %s) AS snapshot", (user_id, current_date))
            row = cur.fetchone()
            
            if row and row[0]:
                try:
                    snapshot_data = json.loads(row[0])
                    results.append(DailySnapshotOut(
                        day=current_date,
                        snapshot=snapshot_data
                    ))
                except json.JSONDecodeError:
                    # Skip invalid JSON
                    pass
            
            current_date += timedelta(days=1)
        
        cur.close()
        return results
    finally:
        cnx.close()

def _overview_common(user_id: int, start: datetime, end: datetime) -> OverviewOut:
    s, e = as_sql_ts(start), as_sql_ts(end)

    latest_hrv = fetch_one(
        "SELECT value FROM hrv WHERE user_id=%s AND start_date < %s ORDER BY start_date DESC LIMIT 1",
        (user_id, e)
    )

    # rolling 7-day HRV baseline within the provided window end
    e_dt = end.astimezone(timezone.utc) if end.tzinfo else end.replace(tzinfo=timezone.utc)
    s7 = as_sql_ts(e_dt - timedelta(days=7))
    avg_hrv_7d = fetch_one(
        "SELECT AVG(value) AS v FROM hrv WHERE user_id=%s AND start_date >= %s AND start_date < %s",
        (user_id, s7, e)
    )

    hr_stats = fetch_one(
        """
        SELECT AVG(avg_value) AS avg_bpm, MIN(min_value) AS min_bpm, MAX(max_value) AS max_bpm
        FROM health_sample
        WHERE user_id=%s AND sample_type='heart_rate' AND start_time >= %s AND end_time < %s
        """,
        (user_id, s, e)
    )

    return OverviewOut(
        window_start=s,
        window_end=e,
        latest_hrv_ms=(latest_hrv["value"] if latest_hrv else None),
        avg_hrv_7d_ms=(avg_hrv_7d["v"] if avg_hrv_7d and avg_hrv_7d["v"] is not None else None),
        latest_hr_avg_bpm=(hr_stats["avg_bpm"] if hr_stats and hr_stats["avg_bpm"] is not None else None),
        hr_min_bpm=(hr_stats["min_bpm"] if hr_stats and hr_stats["min_bpm"] is not None else None),
        hr_max_bpm=(hr_stats["max_bpm"] if hr_stats and hr_stats["max_bpm"] is not None else None),
    )

# Chat endpoints
@app.post("/api/chat/new")
async def create_new_chat(user_id: int = Depends(get_current_user)):
    """Create a new chat session"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available. Please configure GEMINI_API_KEY")
    
    try:
        chat_id = chat_service.create_chat(user_id)
        return {"success": True, "chat_id": chat_id}
    except Exception as e:
        print(f"Error creating chat: {e}")  # Log the actual error
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/list")
async def list_chats(user_id: int = Depends(get_current_user)):
    """Get all chats for current user"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available")
    
    try:
        chats = chat_service.get_user_chats(user_id)
        return {"success": True, "chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: str, user_id: int = Depends(get_current_user)):
    """Get all messages for a chat"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available")
    
    try:
        messages = chat_service.get_chat_messages(chat_id, user_id)
        return {"success": True, "messages": messages}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/{chat_id}/message")
async def send_chat_message(chat_id: str, message_data: ChatMessage, user_id: int = Depends(get_current_user)):
    """Send a message in a chat"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available")
    
    try:
        result = chat_service.send_message(
            chat_id, 
            user_id, 
            message_data.message, 
            message_data.use_health_data,
            message_data.insight_type
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/chat/{chat_id}")
async def delete_chat(chat_id: str, user_id: int = Depends(get_current_user)):
    """Delete a chat and all its messages"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available")
    
    try:
        success = chat_service.delete_chat(chat_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Chat not found")
        return {"success": True, "message": "Chat deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/chat/{chat_id}/rename")
async def rename_chat(chat_id: str, rename_data: ChatRename, user_id: int = Depends(get_current_user)):
    """Rename a chat"""
    if not chat_service:
        raise HTTPException(status_code=503, detail="Chat service not available")
    
    try:
        success = chat_service.rename_chat(chat_id, user_id, rename_data.new_name)
        if not success:
            raise HTTPException(status_code=404, detail="Chat not found")
        return {"success": True, "message": "Chat renamed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static files - must be after all route definitions
@app.get("/static/style.css")
async def serve_css():
    return FileResponse("css/style.css", media_type="text/css")

@app.get("/static/dashboard.js")
async def serve_dashboard_js():
    return FileResponse("js/dashboard.js", media_type="application/javascript")

@app.get("/static/auth.js")
async def serve_auth_js():
    return FileResponse("js/auth.js", media_type="application/javascript")

@app.get("/static/register.js")
async def serve_register_js():
    return FileResponse("js/register.js", media_type="application/javascript")

@app.get("/static/upload.js")
async def serve_upload_js():
    return FileResponse("js/upload.js", media_type="application/javascript")

@app.get("/static/chat.js")
async def serve_chat_js():
    return FileResponse("js/chat.js", media_type="application/javascript")

@app.get("/favicon.ico")
async def serve_favicon():
    return FileResponse("favicon.ico", media_type="image/x-icon")

@app.get("/")
async def serve_login():
    return FileResponse("html/login.html")

@app.get("/register")
async def serve_register():
    return FileResponse("html/register.html")

@app.get("/upload")
async def serve_upload():
    return FileResponse("html/upload.html")

@app.get("/dashboard")
async def serve_dashboard():
    return FileResponse("html/dashboard.html")

@app.get("/static/logo.png")
async def serve_logo():
    return FileResponse("light.png", media_type="image/png")

@app.get("/chat")
async def serve_chat():
    return FileResponse("html/chat.html")

