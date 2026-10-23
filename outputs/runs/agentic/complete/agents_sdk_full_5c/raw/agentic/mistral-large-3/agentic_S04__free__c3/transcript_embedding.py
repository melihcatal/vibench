import os
from sentence_transformers import SentenceTransformer
from speech_models import EmbeddingRequest, EmbeddingResult

def transcript_embedding(request: EmbeddingRequest) -> EmbeddingResult:
    """Embed transcript segments for semantic retrieval using Sentence Transformers (Hugging Face)."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(request.text, convert_to_tensor=False).tolist()
    return EmbeddingResult(embedding=embedding)