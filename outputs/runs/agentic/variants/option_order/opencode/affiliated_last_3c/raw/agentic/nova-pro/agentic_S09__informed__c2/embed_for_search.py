import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def embed_for_search(query, documents):
    query_embedding = generate_embedding(query)
    document_embeddings = generate_batch_embeddings(documents)
    similarities = [
        cosine_similarity(query_embedding, doc_emb) for doc_emb in document_embeddings
    ]
    return similarities
