from sentence_transformers import SentenceTransformer
import numpy as np

def embed_script(script: str, model_name: str = "all-MiniLM-L12-v2") -> np.ndarray:
    """Embed a narration script using a pretrained sentence‑transformer model."""
    model = SentenceTransformer(model_name)
    embeddings = model.encode(script, convert_to_numpy=True)
    return embeddings

if __name__ == "__main__":
    sample = "Welcome to our show where we discuss the latest AI research."
    vec = embed_script(sample)
    print("Embedding shape:", vec.shape)
