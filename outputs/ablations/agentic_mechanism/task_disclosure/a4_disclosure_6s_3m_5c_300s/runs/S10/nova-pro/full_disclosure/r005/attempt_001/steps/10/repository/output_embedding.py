import sentence_transformers

def embed_output(text: str) -> list:
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding.tolist()