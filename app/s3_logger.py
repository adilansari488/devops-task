from datetime import datetime
import os
import boto3
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

s3_client = boto3.client('s3', region_name='eu-west-2')

def logger(record):
    bucket_name = 'devops-task-logging-bucket'
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file_key = f"logs/{timestamp}.json"

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=log_file_key,
            Body=record,
            ContentType='application/json'
        )
        logging.info(f"Successfully logged message to S3: {log_file_key}")
        return f"Successfully logged message to S3: {log_file_key}"
    except Exception as e:
        logging.error(f"Error logging message to S3: {e}")
        return f"Error logging message to S3: {e}"
