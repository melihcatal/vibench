import openai

openai.api_key = "YOUR_API_KEY"


def embed_for_search(query, documents):
    query_embedding = generate_embedding(query)
    document_embeddings = generate_batch_embeddings(documents)
    return query_embedding, document_embeddings
