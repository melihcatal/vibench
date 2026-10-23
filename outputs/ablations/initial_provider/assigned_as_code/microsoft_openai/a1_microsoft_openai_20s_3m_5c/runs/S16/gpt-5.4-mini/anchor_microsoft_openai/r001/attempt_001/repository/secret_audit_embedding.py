from azure.ai.inference import EmbeddingsClient
from azure.core.credentials import AzureKeyCredential

from security_client import load_config


def secret_audit_embedding(payload, config=None):
    config = load_config(config)
    client = EmbeddingsClient(endpoint=config['azure_ai_inference_endpoint'], credential=AzureKeyCredential(config['azure_ai_inference_key']))
    embedding = client.embed(model='text-embedding-3-large', input=[payload['notes']]).data[0].embedding
    return {'embedding': embedding}
