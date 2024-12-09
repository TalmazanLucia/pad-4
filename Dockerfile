# Use the official Python image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /backend

COPY app /backend/app
COPY tests /backend/tests
COPY Dockerfile /backend/Dockerfile
COPY requirements.txt /backend/requirements.txt
COPY run.py /backend/run.py

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Start the Flask app
CMD ["python", "run.py"]
