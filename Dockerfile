# Use the official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Upgrade pip before installing dependencies
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .
