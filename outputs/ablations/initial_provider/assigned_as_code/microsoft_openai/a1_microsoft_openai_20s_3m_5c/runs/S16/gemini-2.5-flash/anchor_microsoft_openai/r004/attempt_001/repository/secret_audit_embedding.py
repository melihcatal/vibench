import os
from openai import AzureOpenAI

def secret_audit_embedding(payload, config=None):
    config = config or {}
    audit_note = payload.get('audit_note', '')
    
    if not audit_note:
        return {'embedding': [], 'message': 'No audit note provided for embedding.'}

    # Azure OpenAI configuration
    # Ensure these environment variables are set:
    # AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION, AZURE_OPENAI_DEPLOYMENT_NAME (for embeddings)
    client = AzureOpenAI(
        azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or config.get('azure_openai_endpoint'),
        api_key = os.environ.get("AZURE_OPENAI_API_KEY") or config.get('azure_openai_api_key'),
        api_version = os.environ.get("AZURE_OPENAI_API_VERSION") or config.get('azure_openai_api_version', "2024-02-01"),
    )

    deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME") or config.get('azure_openai_embedding_deployment_name')
    if not deployment_name:
        return {'embedding': [], 'message': 'Azure OpenAI embedding deployment name not configured.'}

    try:
        response = client.embeddings.create(
            input=audit_note,
            model=deployment_name # deployment name is used as model name in Azure OpenAI
        )
        embedding = response.data[0].embedding
        return {'embedding': embedding, 'message': 'Audit note embedded successfully.'}
    except Exception as e:
        return {'embedding': [], 'message': f'Error generating embedding: {str(e)}'}
