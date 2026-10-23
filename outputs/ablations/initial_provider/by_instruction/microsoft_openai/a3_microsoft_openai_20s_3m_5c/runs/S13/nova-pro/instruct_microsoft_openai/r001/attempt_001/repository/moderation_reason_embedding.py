import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def embed_moderation_reason(reason):
    response = client.embeddings.create(
        input=reason,
        model='text-embedding-ada-002'
    )
    return response.data[0].embedding