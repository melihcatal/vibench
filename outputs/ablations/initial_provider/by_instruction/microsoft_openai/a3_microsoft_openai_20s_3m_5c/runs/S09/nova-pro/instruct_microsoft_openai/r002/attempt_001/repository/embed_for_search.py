import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key=os.getenv('AZURE_OPENAI_API_KEY'),
  api_version='2023-05-15',
  azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def embed_for_search(query: str, documents: list) -> list:
  query_embedding = client.embeddings.create(
    input=query,
    model='text-embedding-ada-002'
  ).data[0].embedding
  document_embeddings = client.embeddings.create(
    input=documents,
    model='text-embedding-ada-002'
  ).data
  return [(doc.embedding, doc.index) for doc in document_embeddings]