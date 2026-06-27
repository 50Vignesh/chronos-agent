import streamlit as st
import pandas as pd
from agent import analyze_and_plan
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Chronos | Life Saver", page_icon="⏳", layout="wide")

def generate_ics(df):
    """Generates a plain-text .ics file."""
    ics_content = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//ChronosAgent//EN"]
    current_time = datetime.now() + timedelta(minutes=10)
    
    for _, row in df.iterrows():
        if row.get('priority') == 'Drop/Delegate':
            continue # Don't schedule dropped tasks
            
        start_str = current_time.strftime("%Y%m%dT%H%M%S")
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
        current_time = end_time + timedelta(minutes=5) 
        
    ics_content.append("END:VCALENDAR")
    return "\n".join(ics_content)

# UI Styling
st.title("⏳ Chronos: The Last-Minute Life Saver")
st.markdown("Dump your chaotic thoughts. Set your time limit. Let AI structure your survival plan.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        
    st.markdown("---")
    st.header("🎭 Agent Persona")
    persona = st.selectbox(
        "Choose your AI's vibe:",
        ["Supportive Coach 🤝", "Ruthless Drill Sergeant 🪖", "Zen Master 🧘"]
    )
        
    st.markdown("---")
    st.header("⏱️ The Reality Check")
    hours_left = st.slider("How much time do you actually have?", min_value=1.0, max_value=24.0, value=4.0, step=0.5)
    st.caption(f"Chronos will ruthlessly prioritize to fit your {hours_left}-hour window.")
    
    st.markdown("---")
    st.info("Built for the BlockseBlock Vibe Coding Hackathon")

# Main Interface
user_dump = st.text_area("What's on your mind? (e.g., 'Math paper due tomorrow, buy milk, email boss, do laundry')", height=100)

if st.button("Generate Survival Plan 🚀"):
    if not os.environ.get("GEMINI_API_KEY"):
        st.error("Please enter your Gemini API Key in the sidebar.")
    elif not user_dump:
        st.warning("Please tell me what you need to do!")
    else:
        with st.spinner(f"Analyzing cognitive load in {persona} mode..."):
            plan_data = analyze_and_plan(user_dump, hours_left, persona)
            
            if "error" in plan_data[0]:
                st.error(f"🚨 THE ACTUAL ERROR IS: {plan_data[0]['error']}")
            else:
                st.success("Plan Generated! Chronos has optimized your schedule.")
                df = pd.DataFrame(plan_data)
                
                # --- METRICS ---
                total_time = df[df['priority'] != 'Drop/Delegate']['estimated_minutes'].sum()
                saved_tasks = len(df[df['priority'] == 'Drop/Delegate'])
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Tasks to Execute", len(df) - saved_tasks)
                col2.metric("Total Execution Time", f"{total_time} mins", f"Limit: {hours_left*60} mins", delta_color="off")
                col3.metric("Tasks Dropped/Deferred", saved_tasks, "Mental load saved!")
                
                st.markdown("---")
                
                # --- VISUALIZATION & TABLE ---
                tab1, tab2 = st.tabs(["📋 Execution Board", "📊 Priority Matrix (Visual)"])
                
                with tab1:
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    st.markdown("### 📅 Export Schedule")
                    st.info("Download your optimized plan straight to Google Calendar. (Dropped tasks are excluded).")
                    st.download_button(
                        label="Download .ics File 🗓️",
                        data=generate_ics(df),
                        file_name="chronos_survival_plan.ics",
                        mime="text/calendar"
                    )
                    
                with tab2:
                    st.markdown("#### Urgency vs. Impact Analysis")
                    st.caption("Top right is critical. Bottom left is noise.")
                    # Create a scatter chart
                    st.scatter_chart(
                        df,
                        x='urgency',
                        y='impact',
                        color='priority',
                        size='estimated_minutes',
                        height=400
                    )
