import os
from openai import AzureOpenAI

def embed_crypto_audit_note(audit_note: str) -> dict:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2023-05-15")
    azure_openai_embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_embedding_deployment_name]):
        raise ValueError("AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, and AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME environment variables must be set.")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )

    response = client.embeddings.create(
        input=[audit_note],
        model=azure_openai_embedding_deployment_name # deployment name for the embedding model
    )

    embedding = response.data[0].embedding
    
    return {"audit_note_embedding": embedding}

