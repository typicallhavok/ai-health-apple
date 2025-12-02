# Health Monitor - Complete Setup

A full-stack health monitoring application with authentication, file upload, and data visualization.

## Features

- **User Authentication** - Login/Register system with password hashing
- **File Upload** - Upload Apple Health export ZIP files
- **Data Visualization** - Interactive charts for HRV, heart rate, activity, and workouts
- **Protected Routes** - All data endpoints require authentication

## Setup

### 1. Update Existing Passwords (if you have existing users)

```bash
mysql -u havok -pmaria apple_health < update_passwords.sql
```

### 2. Start the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or:

```bash
python main.py
```

### 3. Access the Application

Open your browser and go to: `http://localhost:8000`

## User Flow

1. **Login/Register** (`/`) - Landing page with login and registration forms
2. **Upload Data** (`/upload`) - Upload your Apple Health export ZIP file
3. **View Dashboard** (`/dashboard`) - Visualize your health data with interactive charts

## File Structure

```
health-monitor/
├── main.py              # FastAPI backend with auth and upload
├── transfer.py          # Data import script
├── login.html           # Login/Register page
├── upload.html          # File upload page
├── dashboard.html       # Data visualization dashboard
├── auth.js              # Authentication logic
├── upload.js            # File upload logic
├── dashboard.js         # Dashboard logic and charts
├── style.css            # Global styles
├── ddl.txt              # Database schema
└── update_passwords.sql # Password migration script
```

## API Endpoints

### Public Endpoints
- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Protected Endpoints (require HTTP Basic Auth)
- `GET /api/me` - Get current user info
- `POST /api/upload` - Upload and process health data
- `GET /api/users/{user_id}/overview` - Get health overview
- `GET /api/users/{user_id}/hrv/daily` - Get daily HRV data
- `GET /api/users/{user_id}/heart-rate/daily` - Get daily heart rate data
- `GET /api/users/{user_id}/activity/summary` - Get activity summary
- `GET /api/users/{user_id}/workouts` - Get workout data

## How to Export Apple Health Data

1. Open the **Health** app on your iPhone
2. Tap your profile picture in the top right
3. Scroll down and tap **Export All Health Data**
4. Wait for the export to complete (may take a few minutes)
5. Share the ZIP file to your computer
6. Upload it through the web interface

## Security Notes

- Passwords are hashed using SHA-256
- Authentication uses HTTP Basic Auth
- Credentials are stored in localStorage (for demo purposes)
- In production, use HTTPS and proper session management


