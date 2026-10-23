import os
from transformers import AutoModel, AutoTokenizer

model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = AutoModel.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def embed_for_search(query, documents):
    query_embedding = embed_text(query)
    document_embeddings = embed_batch(documents)
    similarities = [cosine_similarity(query_embedding, doc_embedding) for doc_embedding in document_embeddings]
    return similarities