from sentence_transformers import SentenceTransformer

def transcript_embedding(transcript: str):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(transcript)
    return embedding