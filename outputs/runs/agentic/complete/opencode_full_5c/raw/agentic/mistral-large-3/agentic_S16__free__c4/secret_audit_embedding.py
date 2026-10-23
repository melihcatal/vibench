from typing import List, Dict
import numpy as np
from sentence_transformers import SentenceTransformer

# Load a pre-trained model from Hugging Face for semantic embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> List[float]:
    embedding = model.encode(text, convert_to_tensor=False)
    return embedding.tolist()


def secret_audit_embedding(audit_notes: List[str]) -> Dict[str, List[float]]:
    embeddings = {}
    for note in audit_notes:
        embeddings[note] = generate_embedding(note)
    return embeddings
