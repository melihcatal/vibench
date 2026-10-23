from sentence_transformers import SentenceTransformer


def transcript_embedding(transcript):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(transcript)
    return embeddings