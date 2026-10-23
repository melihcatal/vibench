import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15'
)

def embed_rationale(text):
    response = client.embeddings.create(
        input=text,
        model='text-embedding-stable'
    )
    return response.data[0].embedding