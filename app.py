import streamlit as st
import pandas as pd
from agent import analyze_and_plan
import os
from datetime import datetime, timedelta # <-- Added for Calendar formatting

st.set_page_config(page_title="Chronos | Life Saver", page_icon="⏳", layout="wide")

# --- NEW CALENDAR GENERATOR FUNCTION ---
def generate_ics(df):
    """Generates a plain-text .ics file to import tasks directly into Google/Apple Calendar."""
    ics_content = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ChronosAgent//EN"]
    
    # Schedule the first task to start 10 minutes from now
    current_time = datetime.now() + timedelta(minutes=10)
    
    for _, row in df.iterrows():
        start_str = current_time.strftime("%Y%m%dT%H%M%S")
        
        # Default to 30 mins if the LLM forgets to provide an estimate
        duration = int(row.get('estimated_minutes', 30)) 
        end_time = current_time + timedelta(minutes=duration)
        end_str = end_time.strftime("%Y%m%dT%H%M%S")
        
        ics_content.extend([
            "BEGIN:VEVENT",
            f"SUMMARY:{row.get('task_name', 'Task')}",
            f"DESCRIPTION:Action: {row.get('actionable_next_step', '')} | Priority: {row.get('priority', 'Normal')}",
            f"DTSTART:{start_str}",
            f"DTEND:{end_str}",
            "END:VEVENT"
        ])
        
        # Add a 5-minute breather buffer between tasks
        current_time = end_time + timedelta(minutes=5) 
        
    ics_content.append("END:VCALENDAR")
    return "\n".join(ics_content)
# ---------------------------------------

# UI Styling
st.title("⏳ Chronos: The Last-Minute Life Saver")
st.markdown("Dump your chaotic thoughts, deadlines, and panic here. Chronos will intelligently structure your life.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    st.markdown("---")
    st.info("Built with Google AI Studio & Cloud Run")

# Main Interface
user_dump = st.text_area("What's on your mind? (e.g., 'I have a math paper due tomorrow, need to buy milk, and apply for 3 jobs by Friday')", height=150)

if st.button("Generate Action Plan 🚀"):
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not user_dump:
        st.warning("Please tell me what you need to do!")
    else:
        with st.spinner("Analyzing urgency and orchestrating your plan..."):
            plan_data = analyze_and_plan(user_dump)
            
            if "error" in plan_data[0]:
                st.error(f"🚨 THE ACTUAL ERROR IS: {plan_data[0]['error']}")
            else:
                st.success("Plan Generated! Here is your optimized execution strategy:")
                
                df = pd.DataFrame(plan_data)
                
                total_time = df['estimated_minutes'].sum()
                high_priority = len(df[df['priority'] == 'High'])
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Tasks", len(df))
                col2.metric("Critical Actions", high_priority)
                col3.metric("Estimated Time (mins)", total_time)
                
                st.markdown("### 📋 Your Autonomous Execution Board")
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # --- NEW DOWNLOAD BUTTON INTERFACE ---
                st.markdown("### 📅 Export Schedule")
                st.info("Click below to download your action plan and import it directly into Google Calendar.")
                
                ics_data = generate_ics(df)
                st.download_button(
                    label="Download .ics File 🗓️",
                    data=ics_data,
                    file_name="chronos_plan.ics",
                    mime="text/calendar"
                )