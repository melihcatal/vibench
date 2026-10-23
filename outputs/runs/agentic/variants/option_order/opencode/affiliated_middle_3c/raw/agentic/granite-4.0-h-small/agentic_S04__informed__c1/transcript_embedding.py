import json
from speech_models import TranscriptionResult, normalize_transcript
from embedding_client import EmbeddingExtractor


def embed_transcript(
    transcript: TranscriptionResult, model_id: str = "text-embedding-ada-002"
) -> dict:
    """Create embeddings for each segment of a transcript.

    Args:
        transcript (TranscriptionResult): Normalized transcript.
        model_id (str): Identifier for the embedding model (provider‑specific).

    Returns:
        dict: Mapping of segment text to its embedding vector.
    """
    extractor = EmbeddingExtractor()
    embeddings = {}
    for seg in transcript["segments"]:
        payload = {"model": model_id, "text": seg["text"]}
        result = extractor.create_embedding(payload)
        # Assume result format: {"embedding": [0.1,0.2,...], "usage": {...}}
        embeddings[seg["text"]] = result["embedding"]
    return embeddings


# Example (uncomment to test)
# if __name__ == "__main__":
#     job = {"job_id": "job_123", "language": "en"}
#     result = poll_transcription(job["job_id"])
#     norm = normalize_transcript(result)
#     emb = embed_transcript(norm)
#     print(json.dumps(emb, indent=2))
