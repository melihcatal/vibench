from azure.ai.openai import OpenAIClient
from azure.core.credentials import AzureKeyCredential


def secret_audit_embedding(payload, config=None):
    config = config or {}
    client = OpenAIClient(endpoint=config['azure_openai_endpoint'], credential=AzureKeyCredential(config['azure_openai_api_key']))
    response = client.get_embeddings(config['azure_openai_embedding_model'], [payload.get('notes', '')])
    return {'embedding': response.data[0].embedding}
