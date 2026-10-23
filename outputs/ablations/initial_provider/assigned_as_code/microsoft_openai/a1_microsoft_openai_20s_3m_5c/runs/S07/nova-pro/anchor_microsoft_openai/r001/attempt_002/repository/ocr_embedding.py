from sentence_transformers import SentenceTransformer

def embed_text(text):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(text)
    return embeddings