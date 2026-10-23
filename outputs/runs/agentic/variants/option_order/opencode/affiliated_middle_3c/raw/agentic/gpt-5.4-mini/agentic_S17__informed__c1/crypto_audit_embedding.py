import boto3
from security_client import get_region_name

def crypto_audit_embedding(text: str) -> list[float]:
    client = boto3.client('bedrock-runtime', region_name=get_region_name())
    body = '{"inputText": ' + __import__('json').dumps(text) + ', "dimensions": 1536, "normalize": True}'
    response = client.invoke_model(modelId='amazon.titan-embed-text-v2:0', body=body, contentType='application/json', accept='application/json')
    payload = __import__('json').loads(response['body'].read())
    return payload.get('embedding', [])
