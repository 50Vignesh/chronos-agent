Use the official lightweight Python image

FROM python:3.10-slim

Set the working directory inside the container

WORKDIR /app

Copy the requirements file and install dependencies

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

Copy the rest of your application code

COPY . .

Expose the port Streamlit runs on

EXPOSE 8080

Command to run the application

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
