# Chat module for Gemini integration
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from database import fetch_all, fetch_one, get_connection

class HealthDataTool:
    """Tool to fetch health data for the AI assistant"""
    
    @staticmethod
    def get_health_trend_summary(user_id: int, days: int = 14) -> Dict[str, Any]:
        """Get health trend summary using fn_health_trend_summary"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            cur.execute("SELECT fn_health_trend_summary(%s, %s) AS summary", (user_id, days))
            row = cur.fetchone()
            cur.close()
            return {
                "type": "trend_summary",
                "period_days": days,
                "summary": row[0] if row and row[0] else "No trend data available"
            }
        finally:
            cnx.close()
    
    @staticmethod
    def get_health_consistency_score(user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get health consistency score using fn_health_consistency_score"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            cur.execute("SELECT fn_health_consistency_score(%s, %s) AS score", (user_id, days))
            row = cur.fetchone()
            cur.close()
            score = float(row[0]) if row and row[0] else 0.0
            return {
                "type": "consistency_score",
                "period_days": days,
                "score": score,
                "rating": "Excellent" if score >= 80 else "Good" if score >= 60 else "Fair" if score >= 40 else "Needs Improvement"
            }
        finally:
            cnx.close()
    
    @staticmethod
    def get_date_range_suggestion(user_id: int, analysis_type: str = 'trend') -> Dict[str, Any]:
        """Get smart date range suggestion using fn_suggest_date_range"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            cur.execute("SELECT fn_suggest_date_range(%s, %s) AS suggestion", (user_id, analysis_type))
            row = cur.fetchone()
            cur.close()
            if row and row[0]:
                return json.loads(row[0])
            return {"type": "date_suggestion", "error": "No suggestion available"}
        finally:
            cnx.close()
    
    @staticmethod
    def get_correlation_insights(user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get correlation insights using fn_detect_correlations"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            cur.execute("SELECT fn_detect_correlations(%s, %s) AS correlations", (user_id, days))
            row = cur.fetchone()
            cur.close()
            if row and row[0]:
                return json.loads(row[0])
            return {"type": "correlations", "error": "No correlation data available"}
        finally:
            cnx.close()
    
    @staticmethod
    def get_7_day_health_summary(user_id: int) -> Dict[str, Any]:
        """Fetch 7 days of health data for AI analysis"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Fetch HRV data
        hrv_data = fetch_all(
            """
            SELECT DATE(start_date) AS day, AVG(value) AS avg_sdnn_ms
            FROM hrv
            WHERE user_id=%s AND start_date >= %s AND start_date < %s
            GROUP BY DATE(start_date)
            ORDER BY day
            """,
            (user_id, start_date, end_date)
        )
        
        # Fetch heart rate data
        hr_data = fetch_all(
            """
            SELECT DATE(start_time) AS day,
                   AVG(avg_value) AS avg_bpm,
                   MIN(min_value) AS min_bpm,
                   MAX(max_value) AS max_bpm
            FROM health_sample
            WHERE user_id=%s AND sample_type='heart_rate'
              AND start_time >= %s AND end_time < %s
            GROUP BY DATE(start_time)
            ORDER BY day
            """,
            (user_id, start_date, end_date)
        )
        
        # Fetch activity data
        activity_data = fetch_all(
            """
            SELECT date, active_energy_burned, move_time, exercise_time, stand_hours
            FROM activity_summary
            WHERE user_id=%s AND date >= %s AND date < %s
            ORDER BY date
            """,
            (user_id, start_date, end_date)
        )
        
        # Fetch workouts
        workouts = fetch_all(
            """
            SELECT activity_type, duration, total_distance, total_energy_burned,
                   DATE(start_date) as workout_date
            FROM workout
            WHERE user_id=%s AND start_date >= %s AND start_date < %s
            ORDER BY start_date
            """,
            (user_id, start_date, end_date)
        )
        
        return {
            "period": f"{start_date.date()} to {end_date.date()}",
            "hrv": hrv_data,
            "heart_rate": hr_data,
            "activity": activity_data,
            "workouts": workouts
        }

class ChatService:
    """Service for managing chat sessions and Gemini integration"""
    
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        self.health_tool = HealthDataTool()
    
    def create_chat(self, user_id: int, chat_name: str = "Health Chat") -> str:
        """Create a new chat session using stored procedure"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            # Call stored procedure with UUID output
            args = [user_id, '']  # user_id IN, chat_id OUT (VARCHAR)
            result = cur.callproc('sp_create_chat', args)
            chat_id = result[1]  # Get the OUT parameter (UUID string)
            cnx.commit()
            cur.close()
            return chat_id
        finally:
            cnx.close()
    
    def get_user_chats(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all chats for a user"""
        return fetch_all(
            """
            SELECT chat_id, chat_name, created_at, updated_at
            FROM chats
            WHERE user_id=%s
            ORDER BY updated_at DESC
            """,
            (user_id,)
        )
    
    def get_chat_messages(self, chat_id: str, user_id: int) -> List[Dict[str, Any]]:
        """Get all messages for a chat"""
        # Verify chat belongs to user
        chat = fetch_one(
            "SELECT chat_id FROM chats WHERE chat_id=%s AND user_id=%s",
            (chat_id, user_id)
        )
        if not chat:
            raise ValueError("Chat not found or unauthorized")
        
        return fetch_all(
            """
            SELECT message_id, role, content, created_at
            FROM chat
            WHERE chat_id=%s
            ORDER BY created_at
            """,
            (chat_id,)
        )
    
    def delete_chat(self, chat_id: str, user_id: int) -> bool:
        """Delete a chat and all its messages"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            # Verify ownership
            cur.execute(
                "SELECT chat_id FROM chats WHERE chat_id=%s AND user_id=%s",
                (chat_id, user_id)
            )
            if not cur.fetchone():
                return False
            
            # Delete chat (messages cascade)
            cur.execute("DELETE FROM chats WHERE chat_id=%s", (chat_id,))
            cnx.commit()
            cur.close()
            return True
        finally:
            cnx.close()
    
    def rename_chat(self, chat_id: str, user_id: int, new_name: str) -> bool:
        """Rename a chat"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            cur.execute(
                "UPDATE chats SET chat_name=%s WHERE chat_id=%s AND user_id=%s",
                (new_name, chat_id, user_id)
            )
            success = cur.rowcount > 0
            cnx.commit()
            cur.close()
            return success
        finally:
            cnx.close()
    
    def add_message(self, chat_id: str, role: str, content: str, tool_calls: Optional[str] = None) -> bool:
        """Add a message to a chat using stored procedure (prevents duplicates)"""
        cnx = get_connection()
        try:
            cur = cnx.cursor()
            # Call stored procedure that checks for duplicates
            cur.callproc('sp_add_message', [chat_id, role, content])
            cnx.commit()
            cur.close()
            return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
        finally:
            cnx.close()
    
    def send_message(self, chat_id: str, user_id: int, user_message: str, 
                    use_health_data: bool = False, insight_type: str = "raw_data") -> Dict[str, Any]:
        """Send a message and get AI response with optional health insights"""
        # Verify chat ownership
        chat = fetch_one(
            "SELECT chat_id FROM chats WHERE chat_id=%s AND user_id=%s",
            (chat_id, user_id)
        )
        if not chat:
            raise ValueError("Chat not found or unauthorized")
        
        # Save user message
        self.add_message(chat_id, 'user', user_message)
        
        # Get chat history
        messages = self.get_chat_messages(chat_id, user_id)
        
        # Build context for Gemini
        context = self._build_context(messages, user_id, use_health_data, insight_type)
        
        # Get AI response (non-streaming for now)
        try:
            response = self.model.generate_content(context)
            ai_response = response.text
            
            # Save AI response
            self.add_message(chat_id, 'assistant', ai_response)
            
            return {
                "success": True,
                "response": ai_response,
                "used_health_data": use_health_data,
                "insight_type": insight_type if use_health_data else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _build_context(self, messages: List[Dict], user_id: int, 
                      use_health_data: bool, insight_type: str = "raw_data") -> str:
        """Build context string for Gemini with specified insight type"""
        context_parts = []
        
        # System prompt
        context_parts.append(
            "You are a helpful health assistant analyzing Apple Health data. "
            "Provide insightful, actionable advice based on the user's health metrics. "
            "Be supportive, informative, and encouraging. When analyzing data, "
            "look for patterns, trends, and provide specific recommendations."
        )
        
        # Include health data if requested
        if use_health_data:
            try:
                if insight_type == "raw_data":
                    # Last 7 days raw data
                    health_data = self.health_tool.get_7_day_health_summary(user_id)
                    context_parts.append(f"\n\nUser's Last 7 Days Health Data:\n{json.dumps(health_data, indent=2, default=str)}")
                
                elif insight_type == "trend_summary":
                    # Trend summary (14 days)
                    trend_data = self.health_tool.get_health_trend_summary(user_id, 14)
                    context_parts.append(f"\n\nHealth Trend Analysis:\n{json.dumps(trend_data, indent=2, default=str)}")
                
                elif insight_type == "consistency_score":
                    # Consistency score (30 days)
                    consistency_data = self.health_tool.get_health_consistency_score(user_id, 30)
                    context_parts.append(f"\n\nHealth Data Consistency Analysis:\n{json.dumps(consistency_data, indent=2, default=str)}")
                
                elif insight_type == "correlations":
                    # Correlation insights (30 days)
                    correlation_data = self.health_tool.get_correlation_insights(user_id, 30)
                    context_parts.append(f"\n\nHealth Metrics Correlations:\n{json.dumps(correlation_data, indent=2, default=str)}")
                
                elif insight_type == "comprehensive":
                    # All insights combined
                    trend_data = self.health_tool.get_health_trend_summary(user_id, 14)
                    consistency_data = self.health_tool.get_health_consistency_score(user_id, 30)
                    correlation_data = self.health_tool.get_correlation_insights(user_id, 30)
                    
                    context_parts.append(f"\n\nComprehensive Health Analysis:")
                    context_parts.append(f"\n1. Trends (14 days):\n{json.dumps(trend_data, indent=2, default=str)}")
                    context_parts.append(f"\n2. Consistency (30 days):\n{json.dumps(consistency_data, indent=2, default=str)}")
                    context_parts.append(f"\n3. Correlations (30 days):\n{json.dumps(correlation_data, indent=2, default=str)}")
                
            except Exception as e:
                context_parts.append(f"\n\nNote: Could not fetch health insights: {str(e)}")
        
        # Add conversation history (last 10 messages to keep context reasonable)
        context_parts.append("\n\nConversation History:")
        for msg in messages[-10:]:
            role = "User" if msg['role'] == 'user' else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_parts)
