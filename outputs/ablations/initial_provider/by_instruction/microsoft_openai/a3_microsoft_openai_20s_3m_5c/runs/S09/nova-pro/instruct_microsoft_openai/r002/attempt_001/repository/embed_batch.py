import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key=os.getenv('AZURE_OPENAI_API_KEY'),
  api_version='2023-05-15',
  azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def generate_batch_embeddings(texts: list) -> list:
  response = client.embeddings.create(
    input=texts,
    model='text-embedding-ada-002'
  )
  return [item.embedding for item in response.data]