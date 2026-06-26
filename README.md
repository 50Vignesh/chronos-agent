⏳ ChronosAgent: The Last-Minute Life Saver

ChronosAgent is an autonomous, AI-powered productivity companion designed to rescue users from chaotic deadlines, overwhelming assignments, and missed commitments. Built during a vibe-coding hackathon, this tool moves beyond passive reminders to actively help users plan, prioritize, and execute.

🚀 The Problem it Solves

Students, professionals, and entrepreneurs frequently miss deadlines. Existing productivity tools often rely on passive reminders that are easy to ignore.

ChronosAgent tackles this by acting as a proactive assistant. You simply dump your chaotic thoughts and panic into the text box, and the agent uses Google's Gemini 2.5 Flash model to parse, score, and organize them into an actionable, prioritized execution plan.

✨ Key Features

Zero-Friction Brain Dump: Accepts messy, natural language inputs (e.g., "I have a math paper due tomorrow, need to buy milk, and apply for 3 jobs").

Intelligent Task Prioritization: Autonomously calculates Urgency (1-10) and Impact (1-10) to assign priority status (High, Medium, Low).

Micro-Task Breakdown: Breaks down massive, overwhelming tasks into bite-sized, actionable next steps.

Smart Time Estimation: Autonomously estimates the time required for each task in minutes.

One-Click Calendar Export: Generates an .ics (iCalendar) file so you can instantly import your execution plan into Google Calendar or Apple Calendar.

🛠️ Technology Stack

Frontend: Streamlit

Backend Logic: Python, Pandas

AI & LLM: Google Gemini API (gemini-2.5-flash)

Deployment: Docker, Google Cloud Run

💻 How to Run Locally

Clone the repository:

git clone [https://github.com/your-username/chronos-agent.git](https://github.com/your-username/chronos-agent.git)
cd chronos-agent


Install the dependencies:
Make sure you have Python installed, then run:

pip install -r requirements.txt


Run the application:

streamlit run app.py


Add your API Key:
Once the web interface opens in your browser, paste your Google Gemini API Key into the sidebar to activate the AI agent.

🌐 Cloud Deployment

This application is fully containerized with Docker and ready to be deployed on Google Cloud Run for a serverless, highly scalable environment.

Built with ❤️ and Google AI Studio for the Hackathon.
