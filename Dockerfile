FROM python:3.12.4-slim

# Set the working directory
WORKDIR /app

# Copy the wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make wait-for-it script executable
RUN chmod +x /wait-for-it.sh

# Command to run the application, waiting for the database to be available before running Alembic and the app
CMD ["/bin/sh", "-c", "/wait-for-it.sh db:33060 -- alembic upgrade head && python /app/src/main.py"]