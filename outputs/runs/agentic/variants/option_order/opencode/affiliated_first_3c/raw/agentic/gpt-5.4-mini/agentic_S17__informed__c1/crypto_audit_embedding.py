import boto3
from security_models import normalize_text


def crypto_audit_embedding(note: str):
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
    normalized = normalize_text(note)
    result = bedrock.invoke_model(modelId='amazon.titan-embed-text-v2:0', body=normalized.encode('utf-8'))
    return {'provider': 'Amazon Bedrock Runtime', 'model_id': 'amazon.titan-embed-text-v2:0', 'result': str(result)}
