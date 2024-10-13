FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY api.py .
COPY s3_logger.py .
CMD ["python", "api.py"]
# CMD ["gunicorn", "-b", "0.0.0.0:8090", "-w", "4", "api:app"]