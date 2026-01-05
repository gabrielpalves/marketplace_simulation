FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure logs directory exists
RUN mkdir -p logs

# Ensure output is visible in terminal
ENV PYTHONUNBUFFERED=1

CMD ["python", "simulation.py"]