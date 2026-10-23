import os
from openai import AzureOpenAI

def asset_metadata_embedding(payload, config=None):
    config = config or {}
    azure_openai_endpoint = config.get('azure_openai_endpoint')
    azure_openai_key = config.get('azure_openai_key')
    azure_openai_embedding_deployment = config.get('azure_openai_embedding_deployment') # e.g., 'text-embedding-ada-002'
    
    text_to_embed = payload['text']
    # Optionally combine with metadata for richer embeddings
    metadata = payload.get('metadata', {})
    metadata_string = " ".join([f"{k}: {v}" for k, v in metadata.items()])
    combined_text = f"{text_to_embed} {metadata_string}".strip()

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_embedding_deployment]):
        raise ValueError("Azure OpenAI endpoint, key, and embedding deployment must be provided in config.")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01", # Or other supported API version
    )

    try:
        response = client.embeddings.create(
            input=combined_text,
            model=azure_openai_embedding_deployment
        )
        embedding = response.data[0].embedding
    except Exception as e:
        embedding = [] # Return empty list on error

    return {'text': combined_text, 'embedding': embedding}
