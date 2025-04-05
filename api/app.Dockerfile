# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed by some Python packages
# (Example: build-essential for C extensions, though maybe not needed for these specific packages)
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
# Assumes your FastAPI code is in api/app
COPY ./app /app/app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable (optional, if needed by your app)
# ENV NAME World

# Run uvicorn server when the container launches
# Use 0.0.0.0 to ensure it's accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 