# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY lambda_error_monitor.py .

# Install the required dependencies
RUN pip install boto3 flask gunicorn

# Run the app with Gunicorn when the container launches
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "lambda_error_monitor:app"]