from sentence_transformers import SentenceTransformer
from typing import List
from speech_models import EmbeddingResult

EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Hugging Face model

def transcript_embedding(text_segments: List[str]) -> List[EmbeddingResult]:
    """Embed transcript segments for semantic retrieval using Hugging Face Sentence Transformers."""
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(text_segments, convert_to_tensor=False)

    results = []
    for i, embedding in enumerate(embeddings):
        results.append(
            EmbeddingResult(
                embedding=embedding.tolist(),
                text_segment=text_segments[i],
            )
        )
    return results