import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def embed_query_and_documents(query, documents):
    query_embedding = generate_embedding(query)
    document_embeddings = generate_batch_embeddings(documents)
    return query_embedding, document_embeddings

def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model='text-embedding-ada-002'
    )
    return response['data'][0]['embedding']

def generate_batch_embeddings(texts):
    response = openai.Embedding.create(
        input=texts,
        model='text-embedding-ada-002'
    )
    return [item['embedding'] for item in response['data']]