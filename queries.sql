-- ============================================
-- HEALTH MONITOR SYSTEM - SQL QUERIES
-- Complete SQL Script for Database Project
-- ============================================

-- ============================================
-- 1. CREATE STATEMENTS (DDL)
-- ============================================

CREATE DATABASE IF NOT EXISTS apple_health;
USE apple_health;

-- Create USER table
CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100),
    password VARCHAR(255) NOT NULL
);

-- Create HEALTH_RECORD table
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

-- Create METADATA_ENTRY table
CREATE TABLE metadata_entry (
    metadata_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    record_id BIGINT,
    meta_key VARCHAR(255),
    meta_value VARCHAR(255),
    FOREIGN KEY (record_id) REFERENCES health_record(record_id)
);

-- Create HEALTH_SAMPLE table
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

-- Create HRV table
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

-- Create WORKOUT table
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

-- Create ACTIVITY_SUMMARY table
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

-- Create CHATS table
CREATE TABLE chats (
    chat_id VARCHAR(36) PRIMARY KEY,
    user_id INT NOT NULL,
    chat_name VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- Create CHAT_MESSAGES table
CREATE TABLE chat_messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    chat_id VARCHAR(36) NOT NULL,
    role ENUM('user', 'assistant', 'system') NOT NULL,
    content TEXT NOT NULL,
    tool_calls TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chat_id) REFERENCES chats(chat_id) ON DELETE CASCADE
);

-- Create indexes for performance
CREATE INDEX idx_hrv_user_date ON hrv(user_id, start_date);
CREATE INDEX idx_workout_user_date ON workout(user_id, start_date);
CREATE INDEX idx_activity_user_date ON activity_summary(user_id, date);
CREATE INDEX idx_health_record_user_date ON health_record(user_id, start_date);

-- ============================================
-- 2. INSERT STATEMENTS (Sample Data)
-- ============================================

-- Insert sample users (password is SHA-256 hash of 'abcd')
INSERT INTO user (username, name, password)
VALUES 
('havok', 'Akshay', '88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589'),
('john_doe', 'John Doe', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

-- Insert sample health records
INSERT INTO health_record (user_id, type, unit, value, source_name, device, creation_date, start_date, end_date)
VALUES
(1, 'HKQuantityTypeIdentifierHeartRateVariabilitySDNN', 'ms', 45.50, 'Apple Watch', 'iPhone 13', 
 '2024-11-01 10:00:00', '2024-11-01 10:00:00', '2024-11-01 10:01:00'),
(1, 'HKQuantityTypeIdentifierHeartRate', 'count/min', 72.00, 'Apple Watch', 'iPhone 13',
 '2024-11-01 10:00:00', '2024-11-01 10:00:00', '2024-11-01 10:01:00'),
(1, 'HKQuantityTypeIdentifierHeartRate', 'count/min', 68.00, 'Apple Watch', 'iPhone 13',
 '2024-11-01 11:00:00', '2024-11-01 11:00:00', '2024-11-01 11:01:00');

-- Insert sample workouts
INSERT INTO workout (user_id, activity_type, duration, duration_unit, total_distance, total_distance_unit, 
                     total_energy_burned, total_energy_burned_unit, start_date, end_date, source_name)
VALUES
(1, 'HKWorkoutActivityTypeRunning', 30.5, 'min', 5.2, 'km', 350.0, 'kcal', 
 '2024-11-01 07:00:00', '2024-11-01 07:30:30', 'Apple Watch'),
(1, 'HKWorkoutActivityTypeCycling', 45.0, 'min', 15.8, 'km', 420.0, 'kcal',
 '2024-11-02 07:00:00', '2024-11-02 07:45:00', 'Apple Watch');

-- Insert sample activity summaries
INSERT INTO activity_summary (user_id, date, active_energy_burned, move_time, exercise_time, stand_hours)
VALUES
(1, '2024-11-01', 550.5, 180, 45, 12),
(1, '2024-11-02', 620.0, 200, 60, 11),
(1, '2024-11-03', 480.0, 150, 30, 10);

-- ============================================
-- 3. TRIGGERS
-- ============================================

DELIMITER //

-- Trigger 1: Auto-populate HRV table from health_record
DROP TRIGGER IF EXISTS after_insert_health_record //
CREATE TRIGGER after_insert_health_record
AFTER INSERT ON health_record
FOR EACH ROW
BEGIN
  -- Extract HRV (SDNN) measurements
  IF NEW.type = 'HKQuantityTypeIdentifierHeartRateVariabilitySDNN' THEN
    INSERT INTO hrv (user_id, value, unit, creation_date, start_date, end_date)
    VALUES (NEW.user_id, NEW.value, NEW.unit, NEW.creation_date, NEW.start_date, NEW.end_date);
  END IF;

  -- Aggregate heart rate into health_sample
  IF NEW.type = 'HKQuantityTypeIdentifierHeartRate' THEN
    INSERT INTO health_sample
      (user_id, sample_type, avg_value, min_value, max_value, unit, start_time, end_time)
    VALUES (
      NEW.user_id,
      'heart_rate',
      NEW.value,
      NEW.value,
      NEW.value,
      NEW.unit,
      DATE(NEW.start_date),
      DATE(NEW.end_date)
    )
    ON DUPLICATE KEY UPDATE
      avg_value = (avg_value + VALUES(avg_value)) / 2,
      min_value = LEAST(min_value, VALUES(min_value)),
      max_value = GREATEST(max_value, VALUES(max_value));
  END IF;
END //

-- Trigger 2: Append motion context to health records
DROP TRIGGER IF EXISTS after_insert_metadata //
CREATE TRIGGER after_insert_metadata
AFTER INSERT ON metadata_entry
FOR EACH ROW
BEGIN
  IF NEW.meta_key = 'HKMetadataKeyHeartRateMotionContext' THEN
    UPDATE health_record
    SET device = CONCAT(COALESCE(device, ''), ' | MotionContext=', COALESCE(NEW.meta_value, ''))
    WHERE record_id = NEW.record_id;
  END IF;
END //

-- Trigger 3: Cascade delete user data
DROP TRIGGER IF EXISTS before_delete_user //
CREATE TRIGGER before_delete_user
BEFORE DELETE ON user
FOR EACH ROW
BEGIN
  DELETE FROM activity_summary WHERE user_id = OLD.user_id;
  DELETE FROM workout WHERE user_id = OLD.user_id;
  DELETE FROM health_sample WHERE user_id = OLD.user_id;
  DELETE FROM hrv WHERE user_id = OLD.user_id;
  DELETE FROM health_record WHERE user_id = OLD.user_id;
  DELETE FROM chats WHERE user_id = OLD.user_id;
END //

-- Trigger 4: Auto-name chats from first message
DROP TRIGGER IF EXISTS after_insert_first_message //
CREATE TRIGGER after_insert_first_message
AFTER INSERT ON chat_messages
FOR EACH ROW
BEGIN
    DECLARE msg_count INT;
    DECLARE current_name VARCHAR(255);
    
    IF NEW.role = 'user' THEN
        SELECT COUNT(*) INTO msg_count
        FROM chat_messages
        WHERE chat_id = NEW.chat_id AND role = 'user';
        
        SELECT chat_name INTO current_name
        FROM chats
        WHERE chat_id = NEW.chat_id;
        
        IF msg_count = 1 AND current_name = 'Health Chat' THEN
            UPDATE chats
            SET chat_name = LEFT(NEW.content, 50)
            WHERE chat_id = NEW.chat_id;
        END IF;
    END IF;
END //

DELIMITER ;

-- ============================================
-- 4. STORED PROCEDURES
-- ============================================

DELIMITER //

-- Procedure 1: Create new chat session
DROP PROCEDURE IF EXISTS sp_create_chat //
CREATE PROCEDURE sp_create_chat(
    IN p_user_id INT,
    OUT p_chat_id VARCHAR(36)
)
BEGIN
    SET p_chat_id = UUID();
    
    INSERT INTO chats (chat_id, user_id, chat_name)
    VALUES (p_chat_id, p_user_id, 'Health Chat');
    
    INSERT INTO chat_messages (chat_id, role, content)
    VALUES (p_chat_id, 'system', 'Chat started. Ask me anything about your health data!');
END //

-- Procedure 2: Add message with duplicate prevention
DROP PROCEDURE IF EXISTS sp_add_message //
CREATE PROCEDURE sp_add_message(
    IN p_chat_id VARCHAR(36),
    IN p_role ENUM('user', 'assistant', 'system'),
    IN p_content TEXT
)
BEGIN
    DECLARE duplicate_count INT;
    
    -- Check for duplicates in last 5 seconds
    SELECT COUNT(*) INTO duplicate_count
    FROM chat_messages
    WHERE chat_id = p_chat_id
      AND role = p_role
      AND content = p_content
      AND created_at > DATE_SUB(NOW(), INTERVAL 5 SECOND);
    
    IF duplicate_count = 0 THEN
        INSERT INTO chat_messages (chat_id, role, content)
        VALUES (p_chat_id, p_role, p_content);
        
        UPDATE chats SET updated_at = NOW() WHERE chat_id = p_chat_id;
    END IF;
END //

DELIMITER ;

-- ============================================
-- 5. STORED FUNCTIONS
-- ============================================

DELIMITER //

-- Function 1: Get daily health snapshot (JSON)
DROP FUNCTION IF EXISTS fn_user_daily_snapshot //
CREATE FUNCTION fn_user_daily_snapshot(p_user_id INT, p_day DATE)
RETURNS TEXT
DETERMINISTIC
READS SQL DATA
BEGIN
  DECLARE v_avg_hr DECIMAL(10,4);
  DECLARE v_min_hr DECIMAL(10,4);
  DECLARE v_max_hr DECIMAL(10,4);
  DECLARE v_unit VARCHAR(50);
  DECLARE v_avg_sdnn DECIMAL(10,4);
  DECLARE v_mc0 BIGINT DEFAULT 0;
  DECLARE v_mc1 BIGINT DEFAULT 0;

  -- Heart rate aggregates
  SELECT AVG(avg_value), MIN(min_value), MAX(max_value)
    INTO v_avg_hr, v_min_hr, v_max_hr
  FROM health_sample
  WHERE user_id = p_user_id
    AND sample_type = 'heart_rate'
    AND start_time >= p_day
    AND end_time < (p_day + INTERVAL 1 DAY);

  SELECT unit INTO v_unit
  FROM health_sample
  WHERE user_id = p_user_id
    AND sample_type = 'heart_rate'
    AND start_time >= p_day
    AND end_time < (p_day + INTERVAL 1 DAY)
  LIMIT 1;

  -- HRV average
  SELECT AVG(value) INTO v_avg_sdnn
  FROM hrv
  WHERE user_id = p_user_id
    AND start_date >= p_day
    AND start_date < (p_day + INTERVAL 1 DAY);

  -- Motion context counts
  SELECT
    SUM(CASE WHEN me.meta_value = '0' THEN 1 ELSE 0 END),
    SUM(CASE WHEN me.meta_value = '1' THEN 1 ELSE 0 END)
    INTO v_mc0, v_mc1
  FROM metadata_entry me
  JOIN health_record hr ON hr.record_id = me.record_id
  WHERE hr.user_id = p_user_id
    AND me.meta_key = 'HKMetadataKeyHeartRateMotionContext'
    AND hr.start_date >= p_day
    AND hr.start_date < (p_day + INTERVAL 1 DAY);

  RETURN CONCAT(
    '{',
      '"day":"', DATE_FORMAT(p_day, '%Y-%m-%d'), '",',
      '"hr":{',
        '"avg_bpm":', IFNULL(v_avg_hr, 'null'), ',',
        '"min_bpm":', IFNULL(v_min_hr, 'null'), ',',
        '"max_bpm":', IFNULL(v_max_hr, 'null'), ',',
        '"unit":', IFNULL(CONCAT('"', v_unit, '"'), 'null'),
      '},',
      '"hrv":{',
        '"avg_sdnn_ms":', IFNULL(v_avg_sdnn, 'null'),
      '},',
      '"motion_context":{',
        '"0":', IFNULL(v_mc0, 0), ',',
        '"1":', IFNULL(v_mc1, 0),
      '}',
    '}'
  );
END //

DELIMITER ;

-- Function 2: Health trend summary over specified days
DELIMITER //

DROP FUNCTION IF EXISTS fn_health_trend_summary //
CREATE FUNCTION fn_health_trend_summary(
    p_user_id INT,
    p_days INT
) RETURNS TEXT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_hrv_trend VARCHAR(20);
    DECLARE v_hr_trend VARCHAR(20);
    DECLARE v_summary TEXT;
    DECLARE v_hrv_old DECIMAL(10,2);
    DECLARE v_hrv_new DECIMAL(10,2);
    DECLARE v_hr_old DECIMAL(10,2);
    DECLARE v_hr_new DECIMAL(10,2);
    
    -- HRV average for first half of period
    SELECT AVG(value) INTO v_hrv_old
    FROM hrv
    WHERE user_id = p_user_id
    AND start_date BETWEEN DATE_SUB(NOW(), INTERVAL p_days DAY) 
                       AND DATE_SUB(NOW(), INTERVAL p_days/2 DAY);
    
    -- HRV average for second half of period
    SELECT AVG(value) INTO v_hrv_new
    FROM hrv
    WHERE user_id = p_user_id
    AND start_date >= DATE_SUB(NOW(), INTERVAL p_days/2 DAY);
    
    -- Heart rate average for first half of period
    SELECT AVG(avg_value) INTO v_hr_old
    FROM health_sample
    WHERE user_id = p_user_id
    AND sample_type = 'heart_rate'
    AND start_time BETWEEN DATE_SUB(NOW(), INTERVAL p_days DAY) 
                       AND DATE_SUB(NOW(), INTERVAL p_days/2 DAY);
    
    -- Heart rate average for second half of period
    SELECT AVG(avg_value) INTO v_hr_new
    FROM health_sample
    WHERE user_id = p_user_id
    AND sample_type = 'heart_rate'
    AND start_time >= DATE_SUB(NOW(), INTERVAL p_days/2 DAY);
    
    -- Determine HRV trend (>5% change threshold)
    SET v_hrv_trend = CASE 
        WHEN v_hrv_new > v_hrv_old * 1.05 THEN 'improving'
        WHEN v_hrv_new < v_hrv_old * 0.95 THEN 'declining'
        ELSE 'stable'
    END;
    
    -- Determine HR trend (>5% change threshold)
    SET v_hr_trend = CASE 
        WHEN v_hr_new < v_hr_old * 0.95 THEN 'decreasing'
        WHEN v_hr_new > v_hr_old * 1.05 THEN 'increasing'
        ELSE 'stable'
    END;
    
    -- Build summary string
    SET v_summary = CONCAT(
        'HRV: ', COALESCE(ROUND(v_hrv_new, 1), 'N/A'), 'ms (', v_hrv_trend, '), ',
        'HR: ', COALESCE(ROUND(v_hr_new, 1), 'N/A'), 'bpm (', v_hr_trend, ')'
    );
    
    RETURN v_summary;
END //

DELIMITER ;

-- Function 3: Health data consistency score
DELIMITER //

DROP FUNCTION IF EXISTS fn_health_consistency_score //
CREATE FUNCTION fn_health_consistency_score(
    p_user_id INT,
    p_days INT
) RETURNS DECIMAL(5,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_days_with_data INT;
    DECLARE v_score DECIMAL(5,2);
    
    -- Count distinct days with any health data
    SELECT COUNT(DISTINCT DATE(start_date)) INTO v_days_with_data
    FROM (
        SELECT start_date FROM hrv 
        WHERE user_id = p_user_id 
        AND start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY)
        
        UNION
        
        SELECT start_time FROM health_sample 
        WHERE user_id = p_user_id 
        AND start_time >= DATE_SUB(NOW(), INTERVAL p_days DAY)
        
        UNION
        
        SELECT start_date FROM workout 
        WHERE user_id = p_user_id 
        AND start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY)
    ) AS all_dates;
    
    -- Calculate percentage score
    SET v_score = (v_days_with_data / p_days) * 100;
    
    RETURN LEAST(v_score, 100.00);
END //

DELIMITER ;

-- Function 4: Detect health metric correlations
DELIMITER //

DROP FUNCTION IF EXISTS fn_detect_correlations //
CREATE FUNCTION fn_detect_correlations(
    p_user_id INT,
    p_days INT
) RETURNS TEXT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_workout_days INT;
    DECLARE v_high_hrv_days INT;
    DECLARE v_correlation TEXT;
    DECLARE v_avg_hrv_workout DECIMAL(10,2);
    DECLARE v_avg_hrv_rest DECIMAL(10,2);
    
    -- Count days with workouts
    SELECT COUNT(DISTINCT DATE(start_date)) INTO v_workout_days
    FROM workout
    WHERE user_id = p_user_id
    AND start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY);
    
    -- Count days with above-average HRV
    SELECT COUNT(*) INTO v_high_hrv_days
    FROM (
        SELECT DATE(start_date) AS day, AVG(value) AS avg_hrv
        FROM hrv
        WHERE user_id = p_user_id
        AND start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY)
        GROUP BY DATE(start_date)
        HAVING avg_hrv > (
            SELECT AVG(value) FROM hrv 
            WHERE user_id = p_user_id
            AND start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY)
        )
    ) AS high_hrv;
    
    -- Average HRV on workout days
    SELECT AVG(h.value) INTO v_avg_hrv_workout
    FROM hrv h
    WHERE h.user_id = p_user_id
    AND DATE(h.start_date) IN (
        SELECT DISTINCT DATE(start_date) 
        FROM workout 
        WHERE user_id = p_user_id
        AND start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY)
    )
    AND h.start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY);
    
    -- Average HRV on rest days
    SELECT AVG(h.value) INTO v_avg_hrv_rest
    FROM hrv h
    WHERE h.user_id = p_user_id
    AND DATE(h.start_date) NOT IN (
        SELECT DISTINCT DATE(start_date) 
        FROM workout 
        WHERE user_id = p_user_id
        AND start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY)
    )
    AND h.start_date >= DATE_SUB(NOW(), INTERVAL p_days DAY);
    
    -- Build correlation summary
    SET v_correlation = CONCAT(
        'Workout days: ', v_workout_days, '/', p_days, ', ',
        'High HRV days: ', v_high_hrv_days, ', ',
        'Avg HRV (workout): ', COALESCE(ROUND(v_avg_hrv_workout, 1), 'N/A'), 'ms, ',
        'Avg HRV (rest): ', COALESCE(ROUND(v_avg_hrv_rest, 1), 'N/A'), 'ms'
    );
    
    RETURN v_correlation;
END //

DELIMITER ;

-- Function 5: Suggest optimal date range for analysis
DELIMITER //

DROP FUNCTION IF EXISTS fn_suggest_date_range //
CREATE FUNCTION fn_suggest_date_range(
    p_user_id INT,
    p_analysis_type VARCHAR(50)
) RETURNS TEXT
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_oldest_date DATE;
    DECLARE v_newest_date DATE;
    DECLARE v_suggested_days INT;
    DECLARE v_suggestion TEXT;
    
    -- Find oldest and newest data dates
    SELECT 
        MIN(oldest), 
        MAX(newest) 
    INTO v_oldest_date, v_newest_date
    FROM (
        SELECT MIN(DATE(start_date)) AS oldest, MAX(DATE(start_date)) AS newest
        FROM hrv WHERE user_id = p_user_id
        
        UNION ALL
        
        SELECT MIN(DATE(start_time)), MAX(DATE(start_time))
        FROM health_sample WHERE user_id = p_user_id
        
        UNION ALL
        
        SELECT MIN(DATE(start_date)), MAX(DATE(start_date))
        FROM workout WHERE user_id = p_user_id
    ) AS dates;
    
    -- Suggest days based on analysis type
    SET v_suggested_days = CASE p_analysis_type
        WHEN 'quick' THEN 7
        WHEN 'trend' THEN 14
        WHEN 'detailed' THEN 30
        WHEN 'comprehensive' THEN 90
        ELSE 30
    END;
    
    -- Build suggestion
    SET v_suggestion = CONCAT(
        'Suggested: Last ', v_suggested_days, ' days',
        ' (Data available from ', COALESCE(DATE_FORMAT(v_oldest_date, '%Y-%m-%d'), 'N/A'),
        ' to ', COALESCE(DATE_FORMAT(v_newest_date, '%Y-%m-%d'), 'N/A'), ')'
    );
    
    RETURN v_suggestion;
END //

DELIMITER ;

-- ============================================
-- 6. NESTED QUERIES
-- ============================================

-- Nested Query 1: Find users with above-average HRV
SELECT u.username, u.name, avg_hrv.avg_value
FROM user u
JOIN (
    SELECT user_id, AVG(value) AS avg_value
    FROM hrv
    GROUP BY user_id
) AS avg_hrv ON u.user_id = avg_hrv.user_id
WHERE avg_hrv.avg_value > (
    SELECT AVG(value)
    FROM hrv
);

-- Nested Query 2: Users with most workout sessions
SELECT u.username, u.name, workout_count.total_workouts
FROM user u
JOIN (
    SELECT user_id, COUNT(*) AS total_workouts
    FROM workout
    GROUP BY user_id
) AS workout_count ON u.user_id = workout_count.user_id
WHERE workout_count.total_workouts >= (
    SELECT AVG(total_workouts)
    FROM (
        SELECT COUNT(*) AS total_workouts
        FROM workout
        GROUP BY user_id
    ) AS avg_workouts
);

-- Nested Query 3: Find dates with heart rate above user's average
SELECT DATE(start_time) AS day, AVG(avg_value) AS daily_avg
FROM health_sample
WHERE user_id = 1
  AND sample_type = 'heart_rate'
GROUP BY DATE(start_time)
HAVING daily_avg > (
    SELECT AVG(avg_value)
    FROM health_sample
    WHERE user_id = 1 AND sample_type = 'heart_rate'
);

-- Nested Query 4: Users with chats containing more than average messages
SELECT u.username, chat_counts.message_count
FROM user u
JOIN (
    SELECT c.user_id, c.chat_id, COUNT(cm.message_id) AS message_count
    FROM chats c
    JOIN chat_messages cm ON c.chat_id = cm.chat_id
    GROUP BY c.user_id, c.chat_id
) AS chat_counts ON u.user_id = chat_counts.user_id
WHERE chat_counts.message_count > (
    SELECT AVG(message_count)
    FROM (
        SELECT COUNT(*) AS message_count
        FROM chat_messages
        GROUP BY chat_id
    ) AS avg_messages
);

-- ============================================
-- 7. JOIN QUERIES
-- ============================================

-- Join 1: INNER JOIN - Get user health records with metadata
SELECT u.username, hr.type, hr.value, hr.unit, me.meta_key, me.meta_value
FROM user u
INNER JOIN health_record hr ON u.user_id = hr.user_id
INNER JOIN metadata_entry me ON hr.record_id = me.record_id
WHERE u.user_id = 1
ORDER BY hr.start_date DESC
LIMIT 10;

-- Join 2: LEFT JOIN - All users with their HRV averages (including users with no HRV data)
SELECT u.username, u.name, AVG(h.value) AS avg_hrv
FROM user u
LEFT JOIN hrv h ON u.user_id = h.user_id
GROUP BY u.user_id, u.username, u.name;

-- Join 3: Multiple JOIN - User workouts with activity summary on same date
SELECT u.username, 
       w.activity_type, 
       w.duration, 
       w.total_energy_burned,
       a.active_energy_burned AS daily_energy,
       a.exercise_time
FROM user u
JOIN workout w ON u.user_id = w.user_id
JOIN activity_summary a ON u.user_id = a.user_id AND DATE(w.start_date) = a.date
WHERE u.user_id = 1
ORDER BY w.start_date DESC;

-- Join 4: JOIN with aggregation - User chat statistics
SELECT u.username, 
       COUNT(DISTINCT c.chat_id) AS total_chats,
       COUNT(cm.message_id) AS total_messages,
       AVG(msg_per_chat.msg_count) AS avg_messages_per_chat
FROM user u
JOIN chats c ON u.user_id = c.user_id
LEFT JOIN chat_messages cm ON c.chat_id = cm.chat_id
LEFT JOIN (
    SELECT chat_id, COUNT(*) AS msg_count
    FROM chat_messages
    GROUP BY chat_id
) AS msg_per_chat ON c.chat_id = msg_per_chat.chat_id
GROUP BY u.user_id, u.username;

-- Join 5: Complex JOIN - Health records with all related data
SELECT u.username,
       hr.type,
       hr.value,
       hr.unit,
       hr.start_date,
       me.meta_key,
       me.meta_value,
       hs.avg_value AS sample_avg,
       hs.min_value AS sample_min,
       hs.max_value AS sample_max
FROM user u
INNER JOIN health_record hr ON u.user_id = hr.user_id
LEFT JOIN metadata_entry me ON hr.record_id = me.record_id
LEFT JOIN health_sample hs ON u.user_id = hs.user_id 
    AND DATE(hr.start_date) = hs.start_time
WHERE u.user_id = 1
  AND hr.type = 'HKQuantityTypeIdentifierHeartRate'
ORDER BY hr.start_date DESC
LIMIT 20;

-- ============================================
-- 8. AGGREGATE QUERIES
-- ============================================

-- Aggregate 1: Count total records per user
SELECT u.username, 
       COUNT(hr.record_id) AS total_records
FROM user u
LEFT JOIN health_record hr ON u.user_id = hr.user_id
GROUP BY u.user_id, u.username
ORDER BY total_records DESC;

-- Aggregate 2: Average HRV per user with statistics
SELECT u.username,
       COUNT(h.hrv_id) AS hrv_count,
       AVG(h.value) AS avg_hrv,
       MIN(h.value) AS min_hrv,
       MAX(h.value) AS max_hrv,
       STDDEV(h.value) AS stddev_hrv
FROM user u
JOIN hrv h ON u.user_id = h.user_id
GROUP BY u.user_id, u.username
HAVING hrv_count > 5;

-- Aggregate 3: Total workout statistics per user
SELECT u.username,
       COUNT(w.workout_id) AS total_workouts,
       SUM(w.duration) AS total_duration_minutes,
       SUM(w.total_distance) AS total_distance_km,
       SUM(w.total_energy_burned) AS total_calories,
       AVG(w.total_energy_burned) AS avg_calories_per_workout
FROM user u
JOIN workout w ON u.user_id = w.user_id
GROUP BY u.user_id, u.username;

-- Aggregate 4: Monthly activity summary
SELECT u.username,
       DATE_FORMAT(a.date, '%Y-%m') AS month,
       COUNT(*) AS days_logged,
       SUM(a.active_energy_burned) AS monthly_energy,
       AVG(a.move_time) AS avg_move_time,
       AVG(a.exercise_time) AS avg_exercise_time,
       SUM(a.stand_hours) AS total_stand_hours
FROM user u
JOIN activity_summary a ON u.user_id = a.user_id
GROUP BY u.user_id, u.username, DATE_FORMAT(a.date, '%Y-%m')
ORDER BY month DESC;

-- Aggregate 5: Heart rate statistics by day with ranges
SELECT DATE(start_time) AS day,
       COUNT(*) AS reading_count,
       AVG(avg_value) AS daily_avg_hr,
       MIN(min_value) AS daily_min_hr,
       MAX(max_value) AS daily_max_hr,
       MAX(max_value) - MIN(min_value) AS hr_range
FROM health_sample
WHERE user_id = 1
  AND sample_type = 'heart_rate'
  AND start_time >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(start_time)
ORDER BY day DESC;

-- Aggregate 6: Workout activity type breakdown
SELECT u.username,
       w.activity_type,
       COUNT(*) AS workout_count,
       AVG(w.duration) AS avg_duration,
       AVG(w.total_energy_burned) AS avg_calories
FROM user u
JOIN workout w ON u.user_id = w.user_id
GROUP BY u.user_id, u.username, w.activity_type
ORDER BY workout_count DESC;

-- Aggregate 7: Daily health overview with multiple metrics
SELECT DATE(h.start_date) AS day,
       AVG(hrv_data.value) AS avg_hrv,
       AVG(hs.avg_value) AS avg_heart_rate,
       SUM(a.active_energy_burned) AS total_calories,
       COUNT(DISTINCT w.workout_id) AS workout_count
FROM health_record h
LEFT JOIN hrv hrv_data ON DATE(h.start_date) = DATE(hrv_data.start_date) AND h.user_id = hrv_data.user_id
LEFT JOIN health_sample hs ON DATE(h.start_date) = hs.start_time AND h.user_id = hs.user_id AND hs.sample_type = 'heart_rate'
LEFT JOIN activity_summary a ON DATE(h.start_date) = a.date AND h.user_id = a.user_id
LEFT JOIN workout w ON DATE(h.start_date) = DATE(w.start_date) AND h.user_id = w.user_id
WHERE h.user_id = 1
  AND h.start_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
GROUP BY DATE(h.start_date)
ORDER BY day DESC;

-- ============================================
-- 9. COMPLEX ANALYTICAL QUERIES
-- ============================================

-- Query 1: Weekly HRV trend analysis
SELECT 
    WEEK(start_date) AS week_num,
    YEAR(start_date) AS year,
    COUNT(*) AS measurement_count,
    AVG(value) AS avg_hrv,
    STDDEV(value) AS hrv_variability,
    MIN(value) AS min_hrv,
    MAX(value) AS max_hrv
FROM hrv
WHERE user_id = 1
  AND start_date >= DATE_SUB(CURDATE(), INTERVAL 12 WEEK)
GROUP BY YEAR(start_date), WEEK(start_date)
ORDER BY year DESC, week_num DESC;

-- Query 2: Heart rate zones distribution
SELECT 
    CASE 
        WHEN avg_value < 60 THEN 'Resting (<60)'
        WHEN avg_value BETWEEN 60 AND 100 THEN 'Normal (60-100)'
        WHEN avg_value BETWEEN 101 AND 140 THEN 'Elevated (101-140)'
        ELSE 'High (>140)'
    END AS hr_zone,
    COUNT(*) AS reading_count,
    AVG(avg_value) AS avg_in_zone
FROM health_sample
WHERE user_id = 1
  AND sample_type = 'heart_rate'
GROUP BY hr_zone
ORDER BY FIELD(hr_zone, 'Resting (<60)', 'Normal (60-100)', 'Elevated (101-140)', 'High (>140)');

-- Query 3: Workout performance trends
SELECT 
    activity_type,
    DATE_FORMAT(start_date, '%Y-%m') AS month,
    COUNT(*) AS workouts,
    AVG(duration) AS avg_duration,
    AVG(total_distance) AS avg_distance,
    AVG(total_energy_burned) AS avg_calories,
    SUM(total_energy_burned) AS total_calories_month
FROM workout
WHERE user_id = 1
  AND start_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY activity_type, DATE_FORMAT(start_date, '%Y-%m')
ORDER BY month DESC, activity_type;

-- ============================================
-- END OF SQL SCRIPT
-- ============================================
