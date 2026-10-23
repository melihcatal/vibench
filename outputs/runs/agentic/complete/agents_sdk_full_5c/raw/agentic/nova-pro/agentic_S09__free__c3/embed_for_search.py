import os
from huggingface_hub import InferenceApi

api = InferenceApi(repo_id='sentence-transformers/all-MiniLM-L6-v2', token=os.getenv('HUGGINGFACE_API_TOKEN'))

def embed_for_search(query, documents):
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    scores = [similarity_score(query_embedding, doc_emb) for doc_emb in document_embeddings]
    return scores