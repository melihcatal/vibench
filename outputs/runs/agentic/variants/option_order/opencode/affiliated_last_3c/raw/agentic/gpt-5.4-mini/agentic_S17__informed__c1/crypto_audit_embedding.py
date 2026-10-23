import boto3

from security_models import CryptoAuditNote, response_map


def crypto_audit_embedding(note):
    bedrock = boto3.client('bedrock-runtime')
    body = {'inputText': note}
    result = bedrock.invoke_model(modelId='amazon.titan-embed-text-v1', body=str(body).encode('utf-8'))
    return response_map(note=note, embedding_model='amazon.titan-embed-text-v1', result=str(result))
