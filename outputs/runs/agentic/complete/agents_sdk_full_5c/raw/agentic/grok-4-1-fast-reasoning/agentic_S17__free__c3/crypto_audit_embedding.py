import boto3
import json
from typing import List

def embed_crypto_audit_notes(audit_note: str) -> List[float]:
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    body = json.dumps({
        'inputText': audit_note
    })
    response = client.invoke_model(
        modelId='amazon.titan-embed-text-v1',
        body=body,
        contentType='application/json',
        accept='application/json'
    )
    response_body = json.loads(response['body'].read().decode('utf-8'))
    return response_body['embedding']
