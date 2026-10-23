from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_caption_chunks(caption_chunks):
    embeddings = model.encode(caption_chunks, convert_to_numpy=True)
    return np.mean(embeddings, axis=0).tolist()