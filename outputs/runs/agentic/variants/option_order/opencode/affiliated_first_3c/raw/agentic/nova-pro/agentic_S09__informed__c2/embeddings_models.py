from .embed_text import embed_text
from .embed_batch import embed_batch


def normalize_embedding(embedding):
    return embedding / np.linalg.norm(embedding)
