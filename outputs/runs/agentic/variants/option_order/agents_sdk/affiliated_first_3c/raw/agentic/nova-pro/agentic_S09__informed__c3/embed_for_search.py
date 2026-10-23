import openai

openai.api_key = 'your-openai-api-key'

def embed_for_search(query, documents):
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    return query_embedding, document_embeddings