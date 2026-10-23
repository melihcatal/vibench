from sentence_transformers import SentenceTransformer

def embed_platform_output(output):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(output)
    return embeddings