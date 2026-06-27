import google.generativeai as genai
import json
import os
from datetime import datetime

def analyze_and_plan(user_input, hours_available, persona):
    """Takes user text, time limits, and persona to return a structured AI action plan."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
    You are an autonomous productivity agent acting as a {persona}. 
    The current time is {current_time}.
    The user is stressed and has dumped these tasks: "{user_input}"
    
    CRITICAL CONSTRAINT: The user only has {hours_available} hours ({hours_available * 60} minutes) available before their absolute deadline!
    
    Your job:
    1. Break down goals into immediate, actionable micro-tasks.
    2. Assign Urgency (1-10) and Impact (1-10).
    3. Calculate Priority (High, Medium, Low).
    4. Estimate time required in minutes.
    5. REALITY CHECK: If the total time exceeds {hours_available * 60} minutes, you MUST change the priority of the least impactful tasks to "Drop/Delegate" so the remaining tasks fit within the time limit.
    6. TONE: Write the "actionable_next_step" using the voice of a {persona}.
    
    Respond ONLY with a valid JSON array of objects. Keys:
    "task_name", "actionable_next_step", "urgency", "impact", "priority", "estimated_minutes".
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        return [{"error": str(e)}]
