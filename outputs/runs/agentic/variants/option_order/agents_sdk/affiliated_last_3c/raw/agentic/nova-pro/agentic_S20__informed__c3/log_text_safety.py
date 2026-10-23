import os
import boto3

client = boto3.client('comprehend')

def check_safety(log_text):
    response = client.detect_toxic_content(TextSegments=[{"Text": log_text}])
    return response['ResultList'][0]['Toxicity']