# Health Monitor System
## Database Management System Project Report

---

<div style="text-align: center; padding: 50px;">

# HEALTH MONITOR SYSTEM
## AI-Powered Apple Health Data Analytics Platform

### Database Management System Project

---

### Team Details

**Team Name:** [Team Name]

**Team Members:**
1. Amogh E M - PES1UG23AM043
2. Akshay Nadadhur - PES1UG23AM038

**Department:** Computer Science and Engineering - AIML
**Institution:** PES University

</div>

---

# 1. Team details and Problem Statement

## Problem Statement

**Title:** Health Monitor System - AI-Powered Apple Health Data Analytics Platform

### Team Information

| Name | Roll Number |
|------|-------------|
| Amogh E M | PES1UG23AM043 |
| Akshay Nadadhur | PES1UG23AM038 |

---

# 2. Problem Statement Description

## Abstract

In the era of digital health, millions of users generate health data through wearable devices and smartphones, yet lack accessible tools to analyze and derive meaningful insights from this data. The Health Monitor System addresses this critical gap by providing a comprehensive platform for importing, storing, analyzing, and visualizing Apple Health data.

## Problem Definition

Modern health-conscious individuals face several challenges:

1. **Data Inaccessibility**: Apple Health data is locked within the device ecosystem
2. **Limited Analysis**: Native apps provide basic visualizations without deep insights
3. **No Historical Trends**: Difficulty in identifying long-term health patterns
4. **Lack of Intelligent Analysis**: No AI-powered recommendations or correlations
5. **Data Privacy Concerns**: Users want control over their sensitive health information

## Proposed Solution

The Health Monitor System is a full-stack web application that:

- **Imports** Apple Health export files (XML format) seamlessly
- **Stores** structured health data in a normalized MySQL database
- **Visualizes** metrics through interactive charts and dashboards
- **Analyzes** data using AI-powered insights (Google Gemini AI)
- **Secures** user data with authentication and encryption
- **Empowers** users with actionable health recommendations

## Scope

The system handles multiple health metrics:
- Heart Rate Variability (HRV)
- Heart Rate patterns
- Daily Activity (calories, exercise time, stand hours)
- Workout sessions (type, duration, distance, calories)
- Health trends and correlations

---

# 3. User Requirement Specification

## 3.1 Functional Requirements

### FR1: User Management
- **FR1.1** - Users shall be able to register with unique username and password
- **FR1.2** - Users shall be able to login securely with credentials
- **FR1.3** - Passwords shall be hashed using SHA-256 before storage
- **FR1.4** - Users shall be able to delete their account and all associated data
- **FR1.5** - System shall maintain user session state

### FR2: Data Import
- **FR2.1** - System shall accept Apple Health export ZIP files
- **FR2.2** - System shall validate ZIP file format before processing
- **FR2.3** - System shall extract and parse export.xml from ZIP
- **FR2.4** - System shall import health records, workouts, and activity summaries
- **FR2.5** - System shall isolate data per user (multi-tenant support)
- **FR2.6** - System shall provide feedback on import success/failure

### FR3: Data Storage
- **FR3.1** - System shall store user information securely
- **FR3.2** - System shall store health records with timestamps and metadata
- **FR3.3** - System shall aggregate heart rate data automatically
- **FR3.4** - System shall extract HRV measurements separately
- **FR3.5** - System shall maintain referential integrity across tables
- **FR3.6** - System shall support cascade deletion of user data

### FR4: Data Visualization
- **FR4.1** - Dashboard shall display HRV trends over selected date range
- **FR4.2** - Dashboard shall show heart rate statistics (avg, min, max)
- **FR4.3** - Dashboard shall visualize daily activity summaries
- **FR4.4** - Dashboard shall list workout history with details
- **FR4.5** - Users shall be able to select custom date ranges
- **FR4.6** - System shall provide quick filters (7/30/90 days)

### FR5: AI-Powered Chat
- **FR5.1** - Users shall be able to create multiple chat sessions
- **FR5.2** - System shall integrate with Google Gemini AI
- **FR5.3** - Chat shall provide health insights on request
- **FR5.4** - Users shall choose insight type (trends/correlations/comprehensive)
- **FR5.5** - System shall maintain chat history
- **FR5.6** - Users shall be able to rename and delete chats

### FR6: Data Analysis
- **FR6.1** - System shall calculate 7-day HRV averages
- **FR6.2** - System shall detect health trends over 14-day periods
- **FR6.3** - System shall compute consistency scores (30 days)
- **FR6.4** - System shall identify correlations between metrics
- **FR6.5** - System shall generate daily health snapshots

## 3.2 Non-Functional Requirements

### NFR1: Performance
- **NFR1.1** - API response time shall be < 2 seconds for data queries
- **NFR1.2** - Dashboard shall load within 3 seconds
- **NFR1.3** - Data import shall process 10,000 records in < 30 seconds
- **NFR1.4** - Database connection pooling shall support concurrent users

### NFR2: Security
- **NFR2.1** - All passwords shall be hashed using SHA-256
- **NFR2.2** - Protected endpoints shall require authentication
- **NFR2.3** - Users shall only access their own data
- **NFR2.4** - HTTPS shall be enforced in production
- **NFR2.5** - SQL injection shall be prevented using parameterized queries

### NFR3: Scalability
- **NFR3.1** - System shall support minimum 100 concurrent users
- **NFR3.2** - Database shall handle millions of health records
- **NFR3.3** - Connection pool shall auto-scale based on load

### NFR4: Reliability
- **NFR4.1** - System uptime shall be > 99%
- **NFR4.2** - Database backups shall be automated daily
- **NFR4.3** - System shall gracefully handle errors

### NFR5: Usability
- **NFR5.1** - Interface shall be intuitive for non-technical users
- **NFR5.2** - Dashboard shall be responsive across devices
- **NFR5.3** - Error messages shall be clear and actionable

### NFR6: Maintainability
- **NFR6.1** - Code shall follow PEP 8 standards
- **NFR6.2** - Database schema shall be properly documented
- **NFR6.3** - API shall have clear endpoint documentation

## 3.3 Use Cases

### Use Case 1: User Registration and Login
**Actor:** New User  
**Precondition:** None  
**Flow:**
1. User navigates to registration page
2. User enters username, name, and password
3. System validates uniqueness of username
4. System hashes password and creates user account
5. User logs in with credentials
6. System authenticates and grants access

**Postcondition:** User is authenticated and redirected to upload page

### Use Case 2: Import Apple Health Data
**Actor:** Registered User  
**Precondition:** User is logged in  
**Flow:**
1. User navigates to upload page
2. User selects Apple Health export ZIP file
3. System validates file format
4. System extracts and locates export.xml
5. System parses XML and imports data to database
6. Triggers automatically populate HRV and aggregated tables
7. System confirms successful import

**Postcondition:** Health data is stored and accessible in dashboard

### Use Case 3: View Health Dashboard
**Actor:** Registered User  
**Precondition:** User has imported health data  
**Flow:**
1. User navigates to dashboard
2. User selects date range
3. System queries database for metrics
4. System renders interactive charts (HRV, HR, Activity)
5. User explores visualizations

**Postcondition:** User gains insights into health trends

### Use Case 4: Chat with AI Assistant
**Actor:** Registered User  
**Precondition:** User has health data  
**Flow:**
1. User navigates to chat interface
2. User creates new chat or selects existing chat
3. User types health-related question
4. User selects insight type (trends/correlations/raw data)
5. System fetches relevant health data
6. System sends context to Gemini AI
7. AI generates personalized response
8. System displays response to user

**Postcondition:** User receives AI-powered health insights

---

# 4. List of Software/Tools/Programming Languages

## 4.1 Programming Languages

| Language | Version | Usage |
|----------|---------|-------|
| Python | 3.8+ | Backend development, data processing, AI integration |
| JavaScript (ES6+) | - | Frontend interactivity, AJAX requests |
| SQL | MySQL 8.0 | Database queries, stored procedures, triggers |
| HTML5 | - | Page structure and semantic markup |
| CSS3 | - | Styling and responsive design |
| XML | - | Apple Health data format parsing |

## 4.2 Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| FastAPI | 0.104+ | RESTful API framework (ASGI) |
| Uvicorn | 0.24+ | ASGI server for FastAPI |
| mysql-connector-python | 8.2+ | MySQL database driver |
| google-generativeai | Latest | Gemini AI integration |
| python-dotenv | 1.0+ | Environment variable management |
| Pydantic | 2.0+ | Data validation and serialization |

## 4.3 Frontend Technologies

| Technology | Purpose |
|------------|---------|
| Chart.js | Interactive data visualizations (line charts, bar charts) |
| Fetch API | Asynchronous HTTP requests to backend |
| LocalStorage API | Client-side session management |

## 4.4 Database Management System

| Component | Version | Features Used |
|-----------|---------|---------------|
| MySQL | 8.0+ | Relational database management system |
| - Triggers | | Automated data processing (HRV extraction, HR aggregation) |
| - Stored Procedures | | Chat management, message deduplication |
| - Functions | | Daily snapshots, trend analysis |
| - Connection Pooling | | Performance optimization for concurrent access |
| - Foreign Keys | | Referential integrity enforcement |
| - Indexes | | Query optimization |

## 4.5 Development Tools

| Tool | Purpose |
|------|---------|
| VS Code | Primary IDE for development |
| MySQL Workbench | Database design and administration |
| Postman | API testing and documentation |
| Git | Version control |
| GitHub | Code repository and collaboration |
| Chrome DevTools | Frontend debugging |

## 4.6 Third-Party APIs

| API | Purpose | Model/Version |
|-----|---------|---------------|
| Google Gemini AI | Natural language processing and health insights | gemini-2.5-pro |

## 4.7 Libraries and Modules

### Python Libraries
```python
fastapi              # Web framework
uvicorn             # ASGI server
mysql-connector-python  # MySQL driver
google-generativeai    # Gemini AI SDK
python-dotenv          # Environment configuration
pydantic              # Data validation
```

### JavaScript Libraries
```javascript
Chart.js            // Data visualization
// No additional frameworks (Vanilla JS)
```

## 4.8 Installation Commands

```bash
# Python dependencies
pip install -r requirements.txt

# Start application
python main.py
```

---

# 5. ER Diagram

## Entity-Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         HEALTH MONITOR ER DIAGRAM                     │
└─────────────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │     USER     │
                    ├──────────────┤
                    │ *user_id (PK)│
                    │  username    │
                    │  name        │
                    │  password    │
                    └──────┬───────┘
                           │
                           │ 1
                           │
          ┌────────────────┼────────────────┬─────────────────┐
          │                │                │                 │
          │ N              │ N              │ N               │ N
          │                │                │                 │
┌─────────▼────┐  ┌────────▼──────┐  ┌─────▼──────┐  ┌──────▼──────┐
│HEALTH_RECORD │  │HEALTH_SAMPLE  │  │    HRV     │  │   WORKOUT   │
├──────────────┤  ├───────────────┤  ├────────────┤  ├─────────────┤
│*record_id(PK)│  │*sample_id(PK) │  │*hrv_id(PK) │  │*workout_id  │
│ user_id (FK) │  │ user_id (FK)  │  │user_id(FK) │  │ user_id(FK) │
│ type         │  │ sample_type   │  │ value      │  │activity_type│
│ unit         │  │ avg_value     │  │ unit       │  │ duration    │
│ value        │  │ min_value     │  │creation_dt │  │ distance    │
│ source_name  │  │ max_value     │  │ start_date │  │ energy      │
│ device       │  │ unit          │  │ end_date   │  │ start_date  │
│ creation_dt  │  │ start_time    │  └────────────┘  │ end_date    │
│ start_date   │  │ end_time      │                  │ source_name │
│ end_date     │  └───────────────┘                  └─────────────┘
└──────┬───────┘
       │ 1
       │
       │ N
┌──────▼──────────┐
│ METADATA_ENTRY  │
├─────────────────┤
│*metadata_id(PK) │
│ record_id (FK)  │
│ meta_key        │
│ meta_value      │
└─────────────────┘

        ┌──────────────┐
        │     USER     │
        ├──────────────┤
        │ *user_id (PK)│
        └──────┬───────┘
               │ 1
               │
               │ N
        ┌──────▼─────────────┐
        │ ACTIVITY_SUMMARY   │
        ├────────────────────┤
        │ *summary_id (PK)   │
        │  user_id (FK)      │
        │  date              │
        │  active_energy     │
        │  move_time         │
        │  exercise_time     │
        │  stand_hours       │
        └────────────────────┘

        ┌──────────────┐
        │     USER     │
        ├──────────────┤
        │ *user_id (PK)│
        └──────┬───────┘
               │ 1
               │
               │ N
        ┌──────▼──────────┐
        │     CHATS       │
        ├─────────────────┤
        │ *chat_id (PK)   │
        │  user_id (FK)   │
        │  chat_name      │
        │  created_at     │
        │  updated_at     │
        └──────┬──────────┘
               │ 1
               │
               │ N
        ┌──────▼──────────┐
        │ CHAT_MESSAGES   │
        ├─────────────────┤
        │*message_id (PK) │
        │ chat_id (FK)    │
        │ role            │
        │ content         │
        │ tool_calls      │
        │ created_at      │
        └─────────────────┘
```

## 5.1 Entity Descriptions

### USER
**Purpose:** Stores user account information  
**Attributes:**
- `user_id` (PK): Auto-increment unique identifier
- `username`: Unique login username
- `name`: Display name
- `password`: SHA-256 hashed password

### HEALTH_RECORD
**Purpose:** Stores raw Apple Health records  
**Attributes:**
- `record_id` (PK): Auto-increment unique identifier
- `user_id` (FK): Links to USER
- `type`: Health metric type (e.g., HKQuantityTypeIdentifierHeartRate)
- `unit`: Measurement unit
- `value`: Numeric value
- `source_name`: Data source (device/app)
- `device`: Device information
- `creation_date`, `start_date`, `end_date`: Timestamps

### METADATA_ENTRY
**Purpose:** Stores metadata for health records  
**Attributes:**
- `metadata_id` (PK): Auto-increment unique identifier
- `record_id` (FK): Links to HEALTH_RECORD
- `meta_key`: Metadata key (e.g., motion context)
- `meta_value`: Metadata value

### HEALTH_SAMPLE
**Purpose:** Aggregated health samples (primarily heart rate)  
**Attributes:**
- `sample_id` (PK): Auto-increment unique identifier
- `user_id` (FK): Links to USER
- `sample_type`: Type of sample (e.g., heart_rate)
- `avg_value`, `min_value`, `max_value`: Statistical values
- `unit`: Measurement unit
- `start_time`, `end_time`: Time range

### HRV
**Purpose:** Heart Rate Variability measurements  
**Attributes:**
- `hrv_id` (PK): Auto-increment unique identifier
- `user_id` (FK): Links to USER
- `value`: SDNN value in milliseconds
- `unit`: Measurement unit
- `creation_date`, `start_date`, `end_date`: Timestamps

### WORKOUT
**Purpose:** Exercise session details  
**Attributes:**
- `workout_id` (PK): Auto-increment unique identifier
- `user_id` (FK): Links to USER
- `activity_type`: Type of workout
- `duration`, `duration_unit`: Exercise duration
- `total_distance`, `total_distance_unit`: Distance covered
- `total_energy_burned`, `total_energy_burned_unit`: Calories
- `start_date`, `end_date`: Workout timeframe
- `source_name`: Data source

### ACTIVITY_SUMMARY
**Purpose:** Daily activity ring data  
**Attributes:**
- `summary_id` (PK): Auto-increment unique identifier
- `user_id` (FK): Links to USER
- `date`: Calendar date
- `active_energy_burned`: Calories
- `move_time`: Movement minutes
- `exercise_time`: Exercise minutes
- `stand_hours`: Stand hours achieved

### CHATS
**Purpose:** Chat session metadata  
**Attributes:**
- `chat_id` (PK): UUID string
- `user_id` (FK): Links to USER
- `chat_name`: Display name for chat
- `created_at`, `updated_at`: Timestamps

### CHAT_MESSAGES
**Purpose:** Individual messages in chat  
**Attributes:**
- `message_id` (PK): Auto-increment unique identifier
- `chat_id` (FK): Links to CHATS
- `role`: Message role (user/assistant/system)
- `content`: Message text
- `tool_calls`: JSON for tool invocations
- `created_at`: Timestamp

## 5.2 Relationship Descriptions

| Relationship | Cardinality | Description |
|--------------|-------------|-------------|
| USER → HEALTH_RECORD | 1:N | One user has many health records |
| HEALTH_RECORD → METADATA_ENTRY | 1:N | One record has many metadata entries |
| USER → HEALTH_SAMPLE | 1:N | One user has many health samples |
| USER → HRV | 1:N | One user has many HRV measurements |
| USER → WORKOUT | 1:N | One user has many workouts |
| USER → ACTIVITY_SUMMARY | 1:N | One user has many daily activity summaries |
| USER → CHATS | 1:N | One user has many chat sessions |
| CHATS → CHAT_MESSAGES | 1:N | One chat has many messages |

---

# 6. Relational Schema

## 6.1 Table Schemas

### USER
```
USER (user_id INT PK AUTO_INCREMENT,
      username VARCHAR(100) UNIQUE NOT NULL,
      name VARCHAR(100),
      password VARCHAR(255) NOT NULL)
```

### HEALTH_RECORD
```
HEALTH_RECORD (record_id BIGINT PK AUTO_INCREMENT,
               user_id INT FK REFERENCES USER(user_id),
               type VARCHAR(255),
               unit VARCHAR(50),
               value DECIMAL(10,4),
               source_name VARCHAR(255),
               source_version VARCHAR(50),
               device TEXT,
               creation_date DATETIME,
               start_date DATETIME,
               end_date DATETIME)
```

### METADATA_ENTRY
```
METADATA_ENTRY (metadata_id BIGINT PK AUTO_INCREMENT,
                record_id BIGINT FK REFERENCES HEALTH_RECORD(record_id),
                meta_key VARCHAR(255),
                meta_value VARCHAR(255))
```

### HEALTH_SAMPLE
```
HEALTH_SAMPLE (sample_id BIGINT PK AUTO_INCREMENT,
               user_id INT FK REFERENCES USER(user_id),
               sample_type VARCHAR(255),
               avg_value DECIMAL(10,4),
               min_value DECIMAL(10,4),
               max_value DECIMAL(10,4),
               unit VARCHAR(50),
               start_time DATETIME,
               end_time DATETIME,
               UNIQUE(user_id, sample_type, start_time, end_time))
```

### HRV
```
HRV (hrv_id BIGINT PK AUTO_INCREMENT,
     user_id INT FK REFERENCES USER(user_id),
     value DECIMAL(10,4),
     unit VARCHAR(50),
     creation_date DATETIME,
     start_date DATETIME,
     end_date DATETIME)
```

### WORKOUT
```
WORKOUT (workout_id BIGINT PK AUTO_INCREMENT,
         user_id INT FK REFERENCES USER(user_id),
         activity_type VARCHAR(255),
         duration DECIMAL(10,2),
         duration_unit VARCHAR(50),
         total_distance DECIMAL(10,2),
         total_distance_unit VARCHAR(50),
         total_energy_burned DECIMAL(10,2),
         total_energy_burned_unit VARCHAR(50),
         start_date DATETIME,
         end_date DATETIME,
         source_name VARCHAR(255))
```

### ACTIVITY_SUMMARY
```
ACTIVITY_SUMMARY (summary_id BIGINT PK AUTO_INCREMENT,
                  user_id INT FK REFERENCES USER(user_id),
                  date DATE,
                  active_energy_burned DECIMAL(10,2),
                  move_time INT,
                  exercise_time INT,
                  stand_hours INT)
```

### CHATS
```
CHATS (chat_id VARCHAR(36) PK,
       user_id INT FK REFERENCES USER(user_id),
       chat_name VARCHAR(255) NOT NULL,
       created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
       updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)
```

### CHAT_MESSAGES
```
CHAT_MESSAGES (message_id BIGINT PK AUTO_INCREMENT,
               chat_id VARCHAR(36) FK REFERENCES CHATS(chat_id) ON DELETE CASCADE,
               role ENUM('user', 'assistant', 'system') NOT NULL,
               content TEXT NOT NULL,
               tool_calls TEXT,
               created_at DATETIME DEFAULT CURRENT_TIMESTAMP)
```

## 6.2 Functional Dependencies

### USER
- `user_id → username, name, password`
- `username → user_id, name, password`

### HEALTH_RECORD
- `record_id → user_id, type, unit, value, source_name, device, creation_date, start_date, end_date`

### HEALTH_SAMPLE
- `sample_id → user_id, sample_type, avg_value, min_value, max_value, unit, start_time, end_time`
- `{user_id, sample_type, start_time, end_time} → sample_id, avg_value, min_value, max_value, unit`

### HRV
- `hrv_id → user_id, value, unit, creation_date, start_date, end_date`

### WORKOUT
- `workout_id → user_id, activity_type, duration, total_distance, total_energy_burned, start_date, end_date`

### CHATS
- `chat_id → user_id, chat_name, created_at, updated_at`

### CHAT_MESSAGES
- `message_id → chat_id, role, content, tool_calls, created_at`

---

# 7. DDL Commands

## 7.1 Create Database

```sql
CREATE DATABASE IF NOT EXISTS apple_health;
USE apple_health;
```

## 7.2 Create Tables

### USER Table
```sql
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100),
    password VARCHAR(255) NOT NULL
);
```

### HEALTH_RECORD Table
```sql
CREATE TABLE health_record (
    record_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    type VARCHAR(255),
    unit VARCHAR(50),
    value DECIMAL(10,4),
    source_name VARCHAR(255),
    source_version VARCHAR(50),
    device TEXT,
    creation_date DATETIME,
    start_date DATETIME,
    end_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

### METADATA_ENTRY Table
```sql
CREATE TABLE metadata_entry (
    metadata_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    record_id BIGINT,
    meta_key VARCHAR(255),
    meta_value VARCHAR(255),
    FOREIGN KEY (record_id) REFERENCES health_record(record_id)
);
```

### HEALTH_SAMPLE Table
```sql
CREATE TABLE health_sample (
    sample_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    sample_type VARCHAR(255),
    avg_value DECIMAL(10,4),
    min_value DECIMAL(10,4),
    max_value DECIMAL(10,4),
    unit VARCHAR(50),
    start_time DATETIME,
    end_time DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    UNIQUE KEY uq_health_sample (user_id, sample_type, start_time, end_time)
);
```

### HRV Table
```sql
CREATE TABLE hrv (
    hrv_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    value DECIMAL(10,4),
    unit VARCHAR(50),
    creation_date DATETIME,
    start_date DATETIME,
    end_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

### WORKOUT Table
```sql
CREATE TABLE workout (
    workout_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    activity_type VARCHAR(255),
    duration DECIMAL(10,2),
    duration_unit VARCHAR(50),
    total_distance DECIMAL(10,2),
    total_distance_unit VARCHAR(50),
    total_energy_burned DECIMAL(10,2),
    total_energy_burned_unit VARCHAR(50),
    start_date DATETIME,
    end_date DATETIME,
    source_name VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

### ACTIVITY_SUMMARY Table
```sql
CREATE TABLE activity_summary (
    summary_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE,
    active_energy_burned DECIMAL(10,2),
    move_time INT,
    exercise_time INT,
    stand_hours INT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

### CHATS Table
```sql
CREATE TABLE chats (
    chat_id VARCHAR(36) PRIMARY KEY,
    user_id INT NOT NULL,
    chat_name VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);
```

### CHAT_MESSAGES Table
```sql
CREATE TABLE chat_messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chat_id VARCHAR(36) NOT NULL,
    role ENUM('user', 'assistant', 'system') NOT NULL,
    content TEXT NOT NULL,
    tool_calls TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
);
```

## 7.3 Create Indexes

```sql
-- Unique index for health sample deduplication
CREATE UNIQUE INDEX IF NOT EXISTS uq_health_sample
ON health_sample (user_id, sample_type, start_time, end_time);

-- Index for date-based queries
CREATE INDEX idx_hrv_user_date ON hrv(user_id, start_date);
CREATE INDEX idx_workout_user_date ON workout(user_id, start_date);
CREATE INDEX idx_activity_user_date ON activity_summary(user_id, date);
CREATE INDEX idx_health_record_user_date ON health_record(user_id, start_date);
```

## 7.4 Sample Insert

```sql
-- Insert sample user (password is SHA-256 hash of 'abcd')
INSERT INTO user (username, name, password)
VALUES ('havok', 'Akshay', '88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589');
```

---

# 8. CRUD Operation Screenshots

## 8.1 CREATE Operations

### Screenshot 1: User Registration (CREATE)
**Description:** Creating a new user account through the registration interface.

**SQL Query:**
```sql
INSERT INTO user (username, name, password) 
VALUES ('john_doe', 'John Doe', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');
```

![alt text](image-3.png)
```
- Shows: Registration form with username, name, password fields
- Result: Success message "User created successfully"
```

### Screenshot 2: Health Data Import (CREATE)
**Description:** Importing Apple Health data creates thousands of records.

**SQL Query:**
```sql
INSERT INTO health_record 
  (user_id, type, unit, value, source_name, device, creation_date, start_date, end_date)
VALUES 
  (1, 'HKQuantityTypeIdentifierHeartRate', 'count/min', 72.00, 'Apple Watch', 'iPhone', 
   '2024-11-01 10:00:00', '2024-11-01 10:00:00', '2024-11-01 10:01:00');
```

![alt text](image.png)
```
- Shows: File upload interface with ZIP file selected
- Result: "Health data imported successfully" message
```

### Screenshot 3: Create Chat Session (CREATE)
**Description:** Creating a new chat session with AI assistant.

**SQL Query:**
```sql
-- Via stored procedure
CALL sp_create_chat(1, @chat_id);
```

![alt text](image-1.png)

```
- Shows: "New Chat" button and created chat in sidebar
- Result: New chat session with welcome message
```

## 8.2 READ Operations

### Screenshot 4: View Dashboard - HRV Data (READ)
**Description:** Reading and displaying HRV trends over selected date range.

**SQL Query:**
```sql
SELECT DATE(start_date) AS day, AVG(value) AS avg_sdnn_ms
FROM hrv
WHERE user_id = 1 
  AND start_date >= '2024-11-01 00:00:00' 
  AND start_date < '2024-11-30 00:00:00'
GROUP BY DATE(start_date)
ORDER BY day;
```

![alt text](image-2.png)
```
- Shows: Line chart displaying daily HRV values
- Date range selector showing "Last 30 Days"
```

### Screenshot 5: View Heart Rate Statistics (READ)
**Description:** Reading aggregated heart rate data.

**SQL Query:**
```sql
SELECT DATE(start_time) AS day,
       AVG(avg_value) AS avg_bpm,
       MIN(min_value) AS min_bpm,
       MAX(max_value) AS max_bpm,
       unit
FROM health_sample
WHERE user_id = 1 
  AND sample_type = 'heart_rate'
  AND start_time >= '2024-11-01 00:00:00' 
  AND end_time < '2024-11-30 00:00:00'
GROUP BY DATE(start_time), unit
ORDER BY day;
```

![alt text](image-5.png)
```
- Shows: Line chart with average heart rate
- Min/max bands visible
```

### Screenshot 6: View Chat Messages (READ)
**Description:** Reading chat history for a specific chat session.

**SQL Query:**
```sql
SELECT message_id, role, content, created_at
FROM chat_messages
WHERE chat_id = 'abc123-uuid-456def'
ORDER BY created_at;
```
![alt text](image-6.png)
```
- Shows: Chat messages between user and AI assistant
- Multiple messages with timestamps
```

## 8.3 UPDATE Operations

### Screenshot 7: Rename Chat (UPDATE)
**Description:** Updating the name of a chat session.

**SQL Query:**
```sql
UPDATE chats 
SET chat_name = 'HRV Analysis Discussion'
WHERE chat_id = 'abc123-uuid-456def' 
  AND user_id = 1;
```

![alt text](image-9.png)
```
- Shows: Modal with new chat name input
- Result: Chat name updated in sidebar
```

## 8.4 DELETE Operations

### Screenshot 8: Delete Chat Session (DELETE)
**Description:** Deleting a chat and all its messages (cascade).

**SQL Query:**
```sql
DELETE FROM chats 
WHERE chat_id = 'abc123-uuid-456def' 
  AND user_id = 1;

-- Chat messages are automatically deleted due to CASCADE
```

![alt text](image-7.png)
```
- Shows: Confirmation dialog "Are you sure you want to delete this chat?"
- Result: Chat removed from sidebar
```

### Screenshot 9: Delete User Account (DELETE)
**Description:** Deleting user account and all associated data.

**SQL Query:**
```sql
DELETE FROM user 
WHERE user_id = 1;

-- Trigger handles cascade deletion of all user data:
-- - health_record
-- - health_sample
-- - hrv
-- - workout
-- - activity_summary
-- - chats
-- - chat_messages
```

![alt text](image-8.png)
```
- Shows: Account settings with "Delete Account" button
- Confirmation dialog
- Result: User logged out, account deleted
```

# 9. Application Functionalities and Screenshots

## 9.1 User Authentication Module

### Feature 1: User Registration
**Functionality:**
- New users can create accounts with unique username
- Password is hashed (SHA-256) before storage
- Form validation for required fields
- Check for existing username

**Implementation:**
```python
@app.post("/api/register")
async def register(username: str = Form(...), 
                   name: str = Form(...), 
                   password: str = Form(...)):
    # Check if username exists
    # Hash password
    # Create user account
    return {"success": True, "user_id": user_id}
```

![alt text](image-4.png)
```
- Registration form with username, name, password fields
- "Create Account" button
- Link to login page
```

### Feature 2: User Login
**Functionality:**
- Secure login with username and password
- HTTP Basic Authentication
- Session management via localStorage
- Redirect to upload page on success

**Implementation:**
```python
@app.post("/api/login")
async def login(username: str = Form(...), 
                password: str = Form(...)):
    user_id = verify_user(username, password)
    if user_id is None:
        raise HTTPException(status_code=401)
    return {"success": True, "user_id": user_id}
```

![alt text](image-10.png)
```
- Login form with username and password
- "Sign In" button
- Link to registration
```

---

## 9.2 Data Import Module

### Feature 3: Apple Health Data Upload
**Functionality:**
- Accepts Apple Health export ZIP files
- Validates file format
- Extracts and parses export.xml
- Imports data using transfer.py script
- Progress feedback to user

**Implementation:**
```python
@app.post("/api/upload")
async def upload_export(file: UploadFile = File(...), 
                        user_id: int = Depends(get_current_user)):
    # Validate ZIP
    # Extract to user directory
    # Parse XML and import to database
    # Cleanup temporary files
    return {"success": True, "message": "Data imported"}
```

![alt text](image.png)
```
- File upload area with drag-and-drop
- "Select ZIP File" button
- Upload progress indicator
- Success message after import
```

---

## 9.3 Dashboard and Visualization Module

### Feature 4: HRV Trend Visualization
**Functionality:**
- Line chart showing daily HRV (SDNN) values
- Date range selector (7/30/90 days or custom)
- Interactive tooltips on hover
- Responsive chart sizing

**Implementation:**
```javascript
// Fetch HRV data
const hrvData = await fetchHRVData(userId, startDate, endDate);

// Render Chart.js line chart
new Chart(ctx, {
    type: 'line',
    data: {
        labels: hrvData.map(d => d.day),
        datasets: [{
            label: 'HRV (ms)',
            data: hrvData.map(d => d.avg_sdnn_ms)
        }]
    }
});
```

![alt text](image-2.png)
```
- Line chart with daily HRV values
- X-axis: Dates
- Y-axis: HRV in milliseconds
- Date range selector at top
```

### Feature 5: Heart Rate Monitoring
**Functionality:**
- Line chart with average daily heart rate
- Min/max heart rate bands
- Color-coded zones (resting/active)
- Statistical summary

**Implementation:**
```javascript
// Fetch heart rate data with aggregations
const hrData = await fetchHeartRateData(userId, startDate, endDate);

// Render chart with min/max bands
new Chart(ctx, {
    type: 'line',
    data: {
        datasets: [
            { label: 'Average HR', data: hrData.map(d => d.avg_bpm) },
            { label: 'Min HR', data: hrData.map(d => d.min_bpm) },
            { label: 'Max HR', data: hrData.map(d => d.max_bpm) }
        ]
    }
});
```

![alt text](image-5.png)
```
- Multi-line chart showing avg/min/max heart rate
- Shaded area between min and max
- Legend identifying each line
```

### Feature 6: Activity Summary Visualization
**Functionality:**
- Bar chart for daily activity metrics
- Stacked bars for energy/move/exercise/stand
- Goal achievement indicators
- Daily breakdown

**Implementation:**
```javascript
// Fetch activity data
const activityData = await fetchActivitySummary(userId, startDate, endDate);

// Render stacked bar chart
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: activityData.map(d => d.date),
        datasets: [
            { label: 'Active Energy', data: activityData.map(d => d.active_energy_burned) },
            { label: 'Move Time', data: activityData.map(d => d.move_time) },
            { label: 'Exercise Time', data: activityData.map(d => d.exercise_time) }
        ]
    }
});
```

![alt text](image-11.png)
```
- Stacked bar chart for daily activity
- Different colors for each metric
- Legend showing metric types
```

---

## 9.4 AI Chat Assistant Module

### Feature 8: Chat Session Management
**Functionality:**
- Create new chat sessions
- List all user chats in sidebar
- Rename chats
- Delete chats
- Auto-naming from first message

**Implementation:**
```python
@app.post("/api/chat/new")
async def create_new_chat(user_id: int = Depends(get_current_user)):
    chat_id = chat_service.create_chat(user_id)
    return {"success": True, "chat_id": chat_id}

@app.put("/api/chat/{chat_id}/rename")
async def rename_chat(chat_id: str, 
                      rename_data: ChatRename, 
                      user_id: int = Depends(get_current_user)):
    success = chat_service.rename_chat(chat_id, user_id, rename_data.new_name)
    return {"success": success}
```

![alt text](image-1.png)
```
- List of chat sessions with names
- "New Chat" button
- Active chat highlighted
- Rename and delete icons for each chat
```

### Feature 9: AI-Powered Health Insights
**Functionality:**
- Natural language queries about health data
- Multiple insight types (trends/correlations/comprehensive)
- Context-aware responses using Gemini AI
- Health data integration toggle

**Insight Types:**
1. **Raw Data**: Last 7 days of health metrics
2. **Trend Summary**: 14-day pattern analysis
3. **Consistency Score**: 30-day data logging reliability
4. **Correlations**: Relationships between metrics
5. **Comprehensive**: All insights combined

**Implementation:**
```python
@app.post("/api/chat/{chat_id}/message")
async def send_chat_message(chat_id: str, 
                            message_data: ChatMessage, 
                            user_id: int = Depends(get_current_user)):
    result = chat_service.send_message(
        chat_id, 
        user_id, 
        message_data.message, 
        message_data.use_health_data,
        message_data.insight_type
    )
    return result
```

![alt text](image-6.png)
```
- Chat messages showing user questions
- AI assistant responses with health insights
- Toggle for "Use Health Data"
- Dropdown for insight type selection
- Message input area at bottom
```

### Feature 10: Health Data Context for AI
**Functionality:**
- Fetches relevant health data based on insight type
- Formats data as JSON for AI context
- Includes historical trends and statistics
- Provides actionable recommendations

**Implementation:**
```python
class HealthDataTool:
    @staticmethod
    def get_7_day_health_summary(user_id: int):
        # Fetch HRV, heart rate, activity, workouts
        # Return formatted JSON
        pass
    
    @staticmethod
    def get_health_trend_summary(user_id: int, days: int = 14):
        # Analyze trends using stored function
        pass
    
    @staticmethod
    def get_correlation_insights(user_id: int, days: int = 30):
        # Detect correlations between metrics
        pass
```

![alt text](image-12.png)
```
- User asks "How is my HRV trending?"
- AI response with trend analysis
- Mentions specific dates and values
- Provides recommendations
```

---

## 9.5 Data Management Module

### Feature 11: Account Deletion
**Functionality:**
- Delete user account permanently
- Cascade deletion of all health data
- Confirmation dialog for safety
- Immediate logout after deletion

**Implementation:**
```python
@app.delete("/api/user/delete")
async def delete_user(user_id: int = Depends(get_current_user)):
    cnx = get_connection()
    cur = cnx.cursor()
    
    # Delete all user data (cascade)
    cur.execute("DELETE FROM user WHERE user_id = %s", (user_id,))
    
    cnx.commit()
    return {"success": True, "message": "Account deleted"}
```

![alt text](image-8.png)
```
- "Delete Account" button in settings
- Confirmation dialog with warning
- Success message after deletion
```

---

## 9.6 Navigation and UI Features

### Feature 14: Date Range Selection
**Functionality:**
- Quick preset buttons (7/30/90 days)
- Custom date picker
- Real-time chart updates
- Date range validation

![alt text](image-13.png)
```
- Preset buttons: "Last 7 Days", "Last 30 Days", "Last 90 Days"
- Custom date inputs
- "Apply" button
```

---

# 10. Triggers, Procedures/Functions, Nested Queries, Joins, Aggregate Queries

### Purpose

The Health Monitor application addresses the growing need for individuals to understand and analyze their health data. By importing Apple Health export files, users can gain comprehensive insights into their:

- Heart Rate Variability (HRV)
- Daily Heart Rate patterns
- Activity summaries (energy burned, exercise time, stand hours)
- Workout statistics
- Health trends and correlations

### Database Triggers

**1. after_insert_health_record**
- Automatically populates `hrv` table for HRV records
- Aggregates heart rate data into `health_sample` table
- Maintains min/max/average calculations

**2. after_insert_metadata**
- Appends motion context to device field
- Enhances record tracking

**3. before_delete_user**
- Cascade deletion of all user data
- Ensures data privacy and integrity

**4. after_insert_first_message**
- Auto-names chats from first user message
- Improves user experience

### Stored Procedures

**1. sp_create_chat**
- Creates new chat with UUID
- Inserts initial system message
- Returns chat_id

**2. sp_add_message**
- Prevents duplicate messages
- Updates chat timestamp
- Handles concurrent requests

### Stored Functions

**1. fn_user_daily_snapshot**
- Generates daily health snapshot in JSON format with HR, HRV, and motion context
- Aggregates statistics from `health_sample`, `hrv`, and `metadata_entry` tables
- Used by dashboard API to fetch comprehensive daily summaries

**2. fn_health_trend_summary**
- Analyzes HRV and heart rate trends by comparing first half vs second half of period
- Classifies trends as "improving/declining/stable" using 5% threshold
- Returns summary: "HRV: 45.5ms (improving), HR: 72.0bpm (stable)"

**3. fn_health_consistency_score**
- Calculates data logging consistency score (0-100) based on days with health data
- Counts distinct days with HRV, heart rate, or workout records
- Example: 21 days of data in 30 days = 70.00 score

**4. fn_detect_correlations**
- Identifies correlations between workout frequency and HRV levels
- Compares average HRV on workout days vs rest days
- Returns: "Workout days: 12/30, High HRV days: 15, Avg HRV (workout): 48.5ms, Avg HRV (rest): 42.3ms"

**5. fn_suggest_date_range**
- Suggests optimal date range based on analysis type (quick/trend/detailed/comprehensive)
- Recommends 7, 14, 30, or 90 days based on analysis needs
- Returns suggestion with data availability window

---

# 11. Code Snippets for Invoking Procedures/Functions/Triggers

## 11.1 Invoking Triggers

Triggers are automatically executed by the database. Below are examples of operations that invoke them:

### Trigger 1: after_insert_health_record
**Invoked automatically when inserting health records:**
```sql
-- Insert HRV record (automatically populates hrv table)
INSERT INTO health_record (user_id, type, unit, value, source_name, device, creation_date, start_date, end_date)
VALUES (1, 'HKQuantityTypeIdentifierHeartRateVariabilitySDNN', 'ms', 45.50, 'Apple Watch', 'iPhone 13', 
        NOW(), NOW(), NOW());

-- Insert heart rate record (automatically aggregates into health_sample table)
INSERT INTO health_record (user_id, type, unit, value, source_name, device, creation_date, start_date, end_date)
VALUES (1, 'HKQuantityTypeIdentifierHeartRate', 'count/min', 72.00, 'Apple Watch', 'iPhone 13',
        NOW(), NOW(), NOW());
```

### Trigger 2: after_insert_metadata
**Invoked automatically when inserting metadata:**
```sql
-- Insert metadata entry (automatically appends motion context to health_record.device)
INSERT INTO metadata_entry (record_id, meta_key, meta_value)
VALUES (12345, 'HKMetadataKeyHeartRateMotionContext', '1');
```

### Trigger 3: before_delete_user
**Invoked automatically when deleting a user:**
```sql
-- Delete user (automatically cascades to all related tables)
DELETE FROM user WHERE user_id = 1;
```

### Trigger 4: after_insert_first_message
**Invoked automatically when inserting chat message:**
```sql
-- Insert first user message (automatically names the chat)
INSERT INTO chat_messages (chat_id, role, content)
VALUES ('abc123-uuid-456def', 'user', 'How is my HRV trending?');
```

## 11.2 Invoking Stored Procedures

### Procedure 1: sp_create_chat
**Create a new chat session:**
```sql
-- Call procedure to create new chat
CALL sp_create_chat(1, @new_chat_id);

-- Retrieve the generated chat_id
SELECT @new_chat_id AS chat_id;
```

**Python implementation:**
```python
def create_chat(user_id: int) -> str:
    cnx = get_connection()
    cur = cnx.cursor()
    
    # Call stored procedure
    cur.execute("CALL sp_create_chat(%s, @chat_id)", (user_id,))
    cur.execute("SELECT @chat_id")
    chat_id = cur.fetchone()[0]
    
    cnx.commit()
    cur.close()
    cnx.close()
    
    return chat_id
```

### Procedure 2: sp_add_message
**Add message to chat with duplicate prevention:**
```sql
-- Add user message
CALL sp_add_message('abc123-uuid-456def', 'user', 'What is my average heart rate?');

-- Add assistant message
CALL sp_add_message('abc123-uuid-456def', 'assistant', 'Your average heart rate is 72 bpm.');
```

**Python implementation:**
```python
def add_message(chat_id: str, role: str, content: str):
    cnx = get_connection()
    cur = cnx.cursor()
    
    # Call stored procedure (prevents duplicates)
    cur.execute("CALL sp_add_message(%s, %s, %s)", (chat_id, role, content))
    
    cnx.commit()
    cur.close()
    cnx.close()
```

## 11.3 Invoking Stored Functions

### Function 1: fn_user_daily_snapshot
**Get daily health snapshot for a specific date:**
```sql
-- Get snapshot for November 1, 2024
SELECT fn_user_daily_snapshot(1, '2024-11-01') AS daily_snapshot;
```

**Output example:**
```json
{
  "day": "2024-11-01",
  "hr": {"avg_bpm": 72.5, "min_bpm": 58, "max_bpm": 95, "unit": "count/min"},
  "hrv": {"avg_sdnn_ms": 45.5},
  "motion_context": {"0": 120, "1": 45}
}
```

**Python implementation:**
```python
def get_daily_snapshot(user_id: int, date: str) -> dict:
    cnx = get_connection()
    cur = cnx.cursor()
    
    cur.execute("SELECT fn_user_daily_snapshot(%s, %s)", (user_id, date))
    result = cur.fetchone()[0]
    
    cur.close()
    cnx.close()
    
    return json.loads(result)
```

### Function 2: fn_health_trend_summary
**Get health trend analysis:**
```sql
-- Get 14-day trend summary
SELECT fn_health_trend_summary(1, 14) AS trend_summary;

-- Get 30-day trend summary
SELECT fn_health_trend_summary(1, 30) AS trend_summary;
```

**Output example:**
```
HRV: 45.5ms (improving), HR: 72.0bpm (stable)
```

**Python implementation:**
```python
def get_trend_summary(user_id: int, days: int = 14) -> str:
    cnx = get_connection()
    cur = cnx.cursor()
    
    cur.execute("SELECT fn_health_trend_summary(%s, %s) AS summary", (user_id, days))
    result = cur.fetchone()[0]
    
    cur.close()
    cnx.close()
    
    return result
```

### Function 3: fn_health_consistency_score
**Get data logging consistency score:**
```sql
-- Get 30-day consistency score
SELECT fn_health_consistency_score(1, 30) AS consistency_score;
```

**Output example:**
```
70.00
```

**Python implementation:**
```python
def get_consistency_score(user_id: int, days: int = 30) -> float:
    cnx = get_connection()
    cur = cnx.cursor()
    
    cur.execute("SELECT fn_health_consistency_score(%s, %s) AS score", (user_id, days))
    result = cur.fetchone()[0]
    
    cur.close()
    cnx.close()
    
    return float(result)
```

### Function 4: fn_detect_correlations
**Detect correlations between metrics:**
```sql
-- Get 30-day correlation analysis
SELECT fn_detect_correlations(1, 30) AS correlations;
```

**Output example:**
```
Workout days: 12/30, High HRV days: 15, Avg HRV (workout): 48.5ms, Avg HRV (rest): 42.3ms
```

**Python implementation:**
```python
def get_correlation_insights(user_id: int, days: int = 30) -> str:
    cnx = get_connection()
    cur = cnx.cursor()
    
    cur.execute("SELECT fn_detect_correlations(%s, %s) AS correlations", (user_id, days))
    result = cur.fetchone()[0]
    
    cur.close()
    cnx.close()
    
    return result
```

### Function 5: fn_suggest_date_range
**Get date range suggestion:**
```sql
-- Get suggestion for quick analysis
SELECT fn_suggest_date_range(1, 'quick') AS suggestion;

-- Get suggestion for comprehensive analysis
SELECT fn_suggest_date_range(1, 'comprehensive') AS suggestion;
```

**Output example:**
```
Suggested: Last 30 days (Data available from 2024-10-01 to 2024-11-19)
```

**Python implementation:**
```python
def get_date_range_suggestion(user_id: int, analysis_type: str = 'detailed') -> str:
    cnx = get_connection()
    cur = cnx.cursor()
    
    cur.execute("SELECT fn_suggest_date_range(%s, %s) AS suggestion", (user_id, analysis_type))
    result = cur.fetchone()[0]
    
    cur.close()
    cnx.close()
    
    return result
```

## 11.4 Practical Usage Examples

### Example 1: Complete Chat Workflow
```python
# Create new chat session
chat_id = create_chat(user_id=1)

# Add user message
add_message(chat_id, 'user', 'How is my HRV trending?')

# Get trend data for AI context
trend_summary = get_trend_summary(user_id=1, days=14)
consistency = get_consistency_score(user_id=1, days=30)
correlations = get_correlation_insights(user_id=1, days=30)

# Generate AI response (using Gemini)
ai_response = generate_ai_response(trend_summary, consistency, correlations)

# Add assistant response
add_message(chat_id, 'assistant', ai_response)
```

### Example 2: Dashboard Data Loading
```python
# Get date range suggestion
suggestion = get_date_range_suggestion(user_id=1, analysis_type='detailed')

# Get daily snapshots for last 30 days
daily_data = []
for day in last_30_days:
    snapshot = get_daily_snapshot(user_id=1, date=day)
    daily_data.append(snapshot)

# Return to frontend for visualization
return {"daily_data": daily_data, "suggestion": suggestion}
```

### Example 3: Health Report Generation
```python
# Comprehensive health report
report = {
    "trend_14_days": get_trend_summary(user_id=1, days=14),
    "trend_30_days": get_trend_summary(user_id=1, days=30),
    "consistency": get_consistency_score(user_id=1, days=30),
    "correlations": get_correlation_insights(user_id=1, days=30),
    "date_range": get_date_range_suggestion(user_id=1, analysis_type='comprehensive')
}

return report
```

---

# 12. SQL Queries File

All SQL queries used in the project are organized in the file: **`queries.sql`**

## 12.1 File Structure

The `queries.sql` file contains:

### 1. DDL Statements (Data Definition Language)
- `CREATE DATABASE` - Database creation
- `CREATE TABLE` - All table definitions (user, health_record, health_sample, hrv, workout, activity_summary, chats, chat_messages, metadata_entry)
- `CREATE INDEX` - Performance optimization indexes
- `ALTER TABLE` - Schema modifications (if any)

### 2. INSERT Statements (Sample Data)
- Sample user creation with hashed passwords
- Sample health records (HRV, heart rate)
- Sample workouts and activity summaries
- Test data for development

### 3. TRIGGER Definitions
- `after_insert_health_record` - Auto-populate HRV and aggregate heart rate
- `after_insert_metadata` - Append motion context
- `before_delete_user` - Cascade deletion
- `after_insert_first_message` - Auto-name chats

### 4. STORED PROCEDURE Definitions
- `sp_create_chat` - Create new chat session with UUID
- `sp_add_message` - Add message with duplicate prevention

### 5. STORED FUNCTION Definitions
- `fn_user_daily_snapshot` - Daily health summary JSON
- `fn_health_trend_summary` - Trend analysis
- `fn_health_consistency_score` - Consistency scoring
- `fn_detect_correlations` - Correlation detection
- `fn_suggest_date_range` - Date range suggestions

### 6. NESTED QUERIES
- Find users with above-average HRV
- Users with most workout sessions
- Dates with heart rate above user's average
- Users with chats containing more than average messages

### 7. JOIN QUERIES
- `INNER JOIN` - User health records with metadata
- `LEFT JOIN` - All users with HRV averages (including null)
- Multiple `JOIN` - User workouts with activity summary
- Complex `JOIN` - Health records with all related data
- `JOIN` with aggregation - User chat statistics

### 8. AGGREGATE QUERIES
- `COUNT` - Total records per user
- `AVG`, `MIN`, `MAX`, `STDDEV` - HRV statistics
- `SUM` - Total workout statistics
- `GROUP BY` - Monthly activity summaries
- Complex aggregation - Daily health overview with multiple metrics
- Weekly/monthly trend analysis

### 9. ANALYTICAL QUERIES
- Weekly HRV trend analysis with `WEEK()` and `YEAR()`
- Heart rate zones distribution with `CASE` statements
- Workout performance trends by activity type
- Time-series analysis queries

## 12.2 File Location

```
health-monitor/
├── queries.sql           ← Complete SQL script file
├── main.py
├── database.py
├── chat_service.py
├── transfer.py
└── ...
```

## 12.3 How to Use queries.sql

### Execute Complete Setup
```bash
# Run entire script to set up database
mysql -u root -p < queries.sql
```

### Execute Specific Sections
```bash
# Run only DDL statements
mysql -u root -p apple_health < queries.sql --init-command="SET autocommit=0"

# Run specific queries interactively
mysql -u root -p apple_health
source queries.sql;
```

### Import in MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. File → Open SQL Script → Select `queries.sql`
4. Execute script using the lightning bolt icon

## 12.4 Query Categories Summary

| Category | Count | Examples |
|----------|-------|----------|
| CREATE Statements | 9 tables | user, health_record, hrv, workout, chats, etc. |
| INSERT Statements | 10+ | Sample users, health records, workouts |
| Triggers | 4 | Auto-populate HRV, cascade delete, auto-name chats |
| Procedures | 2 | Create chat, add message |
| Functions | 5 | Daily snapshot, trends, consistency, correlations |
| Nested Queries | 4+ | Above-average HRV users, workout leaders |
| Join Queries | 5+ | User-health data joins, multi-table aggregations |
| Aggregate Queries | 7+ | Statistics, summaries, trend analysis |

## 12.5 Key SQL Patterns Used

### Pattern 1: Conditional Aggregation
```sql
SUM(CASE WHEN condition THEN 1 ELSE 0 END)
```

### Pattern 2: Temporal Analysis
```sql
DATE_SUB(NOW(), INTERVAL n DAY)
DATE_FORMAT(date_column, '%Y-%m')
```

### Pattern 3: Subquery in JOIN
```sql
FROM table1 t1
JOIN (SELECT ... FROM table2 GROUP BY ...) AS t2 ON t1.id = t2.id
```

### Pattern 4: Window Functions Alternative
```sql
-- Using subqueries for comparison with averages
HAVING avg_value > (SELECT AVG(value) FROM table WHERE ...)
```

### Pattern 5: JSON Construction
```sql
CONCAT('{', '"key":', value, ',', '"key2":', value2, '}')
```

---

