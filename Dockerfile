FROM python:3.11.6-alpine3.18
LABEL authors="antony"

# Set Python to flush output immediately
ENV PYTHONUNBUFFERED=1

# Set up working directory
WORKDIR app/

# Upgrade pip first for stability
RUN pip install --no-cache-dir --upgrade pip

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .



# Default command or entrypoint can be added here if needed
