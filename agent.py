import google.generativeai as genai
import json
import os
from datetime import datetime

def analyze_and_plan(user_input, hours_available, persona):
    """Takes user text, time limits, and persona to return a structured AI action plan."""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    # Using Gemini 2.5 Flash for speed and complex JSON structuring
    model = genai.GenerativeModel('gemini-2.5-flash')
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
    You are an autonomous productivity agent acting as a {persona}. 
    The current time is {current_time}.
    The user has dumped these chaotic tasks: "{user_input}"
    
    CRITICAL CONSTRAINT: The user only has {hours_available} hours ({hours_available * 60} minutes) available before their deadline!
    
    Your job:
    1. Break down goals into immediate, actionable micro-tasks.
    2. Assign Urgency (1-10) and Impact (1-10) to calculate Priority (High, Medium, Low).
    3. Estimate time required in minutes.
    4. REALITY CHECK: If the total time exceeds {hours_available * 60} minutes, change the priority of the least impactful tasks to "Drop/Delegate".
    5. THE CHEAT CODE: For every task, provide a "smart_shortcut" to do it 2x faster. **You must highly prioritize suggesting Google Ecosystem Tools** (e.g., Google Scholar, Google Workspace, Google Keep, Google Maps, Gemini, etc.) where applicable.
    6. AGENTIC BEHAVIOR (Fatigue Management): If the total execution time is over 90 minutes, you MUST autonomously create and insert a task named "Cognitive Rest Block" for 15 minutes to prevent burnout.
    7. Write the "actionable_next_step" using the voice of a {persona}.
    
    Respond ONLY with a valid JSON array of objects. Keys MUST exactly match:
    "task_name", "actionable_next_step", "smart_shortcut", "urgency", "impact", "priority", "estimated_minutes".
    """
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        return [{"error": str(e)}]
