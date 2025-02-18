# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Create directory for our app
WORKDIR /app

# Copy the script and sample CSV into the image
COPY netcheck/netcheck.py /app/netcheck.py
COPY netcheck/input.csv /netcheck/input.csv

# Make the script executable
RUN chmod +x /app/netcheck.py

# Set up any Python dependencies if needed (none in this minimal example)
# RUN pip install --no-cache-dir ...

# The default timeout for network checks (can be overridden at runtime)
ENV TIMEOUT=10

# By default, the container will just run the netcheck script
ENTRYPOINT ["/app/netcheck.py"]
