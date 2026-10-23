import os
from typing import Any, Dict, List

import boto3

AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'amazon.nova-lite-v1:0')


def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    client = boto3.client('bedrock-runtime', region_name=AWS_REGION)
    prompt = {'events': events}
    response = client.converse(modelId=BEDROCK_MODEL_ID, messages=[{'role': 'user', 'content': [{'text': str(prompt)}]}])
    return response['output']['message']['content'][0]['text']
