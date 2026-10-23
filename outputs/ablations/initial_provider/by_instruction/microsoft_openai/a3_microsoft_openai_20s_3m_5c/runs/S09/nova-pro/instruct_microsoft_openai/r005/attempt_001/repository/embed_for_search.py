import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def embed_for_search(query: str, documents: list[str]) -> tuple[list[float], list[list[float]]]:
    query_embedding = generate_embedding(query)
    document_embeddings = generate_batch_embeddings(documents)
    return query_embedding, document_embeddings

def generate_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model='text-embedding-ada-002'
    )
    return response.data[0].embedding

def generate_batch_embeddings(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        input=texts,
        model='text-embedding-ada-002'
    )
    return [data.embedding for data in response.data]