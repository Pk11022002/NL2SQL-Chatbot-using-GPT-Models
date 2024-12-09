# Dockerfile
FROM python:3.12

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install chromadb
RUN pip install chromadb

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py"]
