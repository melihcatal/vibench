from sentence_transformers import SentenceTransformer

def asset_metadata_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text)
    print(f"Embedding: {embedding}")
    return embedding
