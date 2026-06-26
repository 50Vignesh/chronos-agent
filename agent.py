import google.generativeai as genai
import json
import os
from datetime import datetime

def analyze_and_plan(user_input):
    """Takes user text and returns a structured AI action plan."""
    
    # Configure the API key dynamically right when the button is clicked!
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 🔴 FIX: Upgraded to Gemini 2.5 Flash (1.5 models are deprecated)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
    You are an autonomous productivity agent. The current time is {current_time}.
    The user is stressed and has dumped the following tasks/thoughts:
    "{user_input}"
    
    Your job is to act as a Last-Minute Life Saver. 
    1. Break down complex goals into immediate, actionable micro-tasks.
    2. Assign an urgency score (1-10) and an impact score (1-10).
    3. Calculate a priority status (High, Medium, Low).
    4. Estimate the time required for each task in minutes.
    
    Respond ONLY with a valid JSON array of objects. Each object must have the following keys:
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