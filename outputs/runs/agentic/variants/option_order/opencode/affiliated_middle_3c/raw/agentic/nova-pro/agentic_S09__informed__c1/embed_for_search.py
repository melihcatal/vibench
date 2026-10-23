import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_for_semantic_search(query, documents):
    query_embedding = generate_embedding(query)
    document_embeddings = generate_batch_embeddings(documents)
    similarities = [
        cosine_similarity(query_embedding, doc_embedding)
        for doc_embedding in document_embeddings
    ]
    return similarities
