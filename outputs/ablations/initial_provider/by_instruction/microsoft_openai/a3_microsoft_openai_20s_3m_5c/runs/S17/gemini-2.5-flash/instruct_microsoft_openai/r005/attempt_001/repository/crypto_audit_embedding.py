import os
from openai import AzureOpenAI

def embed_audit_note(audit_note: str, azure_openai_endpoint: str, azure_openai_key: str, embedding_model_name: str) -> list[float]:
    """
    Embeds crypto audit notes for semantic search using Azure OpenAI.
    """
    # Initialize the Azure OpenAI client
    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01"
    )

    # Create embedding for the audit note
    response = client.embeddings.create(
        input=audit_note,
        model=embedding_model_name # e.g., "text-embedding-ada-002" or a deployed model name
    )
    
    # The embedding is a list of floats
    embedding = response.data[0].embedding
    return embedding
