from flask import Flask, jsonify, abort
import json
import boto3
import requests
from flask_cors import CORS
from s3_logger import logger
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
CORS(app)

sns_topic_arn = 'arn:aws:sns:eu-west-2:146366115606:devops-task-sns'
sns_client = boto3.client('sns', region_name='eu-west-2')

@app.route('/devops-task/publish', methods=['GET'])
def publish():
    sample_api_url = 'https://api.sampleapis.com/coffee/hot'
    
    try:
        response = requests.get(sample_api_url)
        data = response.json()
        logging.info(f'Data received from API: {data}')
        sns_response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(data),
            Subject='New Data from Sample API'
        )
        logger(json.dumps(sns_response))
        return jsonify({
            'message': 'Data sent to SNS topic successfully',
            'Response': sns_response
        }), 200
    
    except Exception as e:
        logging.error({
            'message': 'Failed to fetch data or publish to SNS',
            'error': str(e)})
        return jsonify({
            'message': 'Failed to fetch data or publish to SNS',
            'error': str(e)
        }), 500

def drop_all(path):
    abort(502)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8090)
