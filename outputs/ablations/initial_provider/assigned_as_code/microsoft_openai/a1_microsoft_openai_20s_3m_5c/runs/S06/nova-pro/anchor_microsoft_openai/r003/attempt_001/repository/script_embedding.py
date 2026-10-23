import sentence_transformers as sentence_transformers

def embed_text(text):
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([text])
    return embeddings[0]