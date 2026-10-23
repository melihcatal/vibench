import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def embed_query_and_documents(query, documents):
    query_embedding = client.embeddings.create(input=query, model='text-embedding-ada-002').data[0].embedding
    document_embeddings = client.embeddings.create(input=documents, model='text-embedding-ada-002').data
    return query_embedding, [doc.embedding for doc in document_embeddings]