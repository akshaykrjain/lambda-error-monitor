# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY lambda_error_monitor.py .

# Install the required dependencies
RUN pip install boto3 flask

# Expose the port for health check
EXPOSE 8080

# Run the script when the container launches
CMD ["python", "lambda_error_monitor.py"]