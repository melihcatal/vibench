from openai import AzureOpenAI

from model_client import build_azure_openai_client


def platform_output_embedding(text: str):
    client = build_azure_openai_client()
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
