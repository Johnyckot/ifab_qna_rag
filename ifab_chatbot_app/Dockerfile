# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . /app

# Expose the port the app runs on
EXPOSE 8501

# Set the command to start the container
CMD ["streamlit", "run", "ifab_chatbot_app.py"]