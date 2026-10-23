from sentence_transformers import SentenceTransformer
from typing import List

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_script(script: str) -> List[float]:
    embedding = model.encode(script, convert_to_tensor=False)
    return embedding.tolist()