import boto3
import json
import time

def get_client(service_name):
    return boto3.client(service_name, region_name='us-west-2')

def normalize_log_event(log_event):
    return {
        'timestamp': int(time.time() * 1000),
        'message': json.dumps(log_event)
    }