FROM python:3.13-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py config.py leet_logger.py ./

# Environment variables
ENV RESEND_API_KEY=""
ENV CRON_USERNAME="admin"
ENV CRON_PASSWORD="admin"

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
