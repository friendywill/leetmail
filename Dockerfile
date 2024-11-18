FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .
COPY config.yml .

# Environment variables
ENV RESEND_API_KEY=""
ENV CRON_USERNAME="admin"
ENV CRON_PASSWORD="admin"

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
