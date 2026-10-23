from embeddings_client import client

def create_embedding(text):
    return client.embeddings.create(input=text, model='text-embedding-ada-002').data[0].embedding

def create_batch_embeddings(texts):
    return [item.embedding for item in client.embeddings.create(input=texts, model='text-embedding-ada-002').data]