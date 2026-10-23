from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def secret_audit_embedding(audit_notes: List[str]) -> List[List[float]]:
    embeddings = model.encode(audit_notes, convert_to_numpy=True)
    return embeddings.tolist()
