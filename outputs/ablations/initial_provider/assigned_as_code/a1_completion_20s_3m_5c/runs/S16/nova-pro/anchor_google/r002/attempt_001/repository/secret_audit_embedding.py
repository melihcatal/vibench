import boto3
from sentence_transformers import SentenceTransformer


def embed_secret_audit_notes(payload):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=payload['secret_id'])
    audit_notes = response['SecretString']
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(audit_notes)
    return {'embeddings': embeddings.tolist()}