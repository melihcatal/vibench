import os
from openai import AzureOpenAI

def embed_moderation_reason(reason_text: str, config: dict) -> list[float]:
    client = AzureOpenAI(
        azure_endpoint=config['azure_openai_endpoint'],
        api_key=config['azure_openai_api_key'],
        api_version=config.get('azure_openai_api_version', "2023-05-15"),
    )
    response = client.embeddings.create(
        input=reason_text,
        model=config['azure_openai_embedding_deployment_name']
    )
    return response.data[0].embedding
