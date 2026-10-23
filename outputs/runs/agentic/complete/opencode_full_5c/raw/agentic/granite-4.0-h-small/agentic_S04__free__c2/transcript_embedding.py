import json
from typing import List, Dict
from speech_models import TranscriptionSegment


def transcript_embedding(segments: List[TranscriptionSegment]) -> List[Dict[str, any]]:
    """Generate embeddings for each transcription segment for semantic retrieval.

    Returns a list of dictionaries containing the segment text and a placeholder embedding vector.
    In a real implementation, call a model like OpenAI's `text-embedding-ada-002`.
    """
    embeddings = []
    for seg in segments:
        # Placeholder embedding: 1536-dimensional zero vector
        placeholder_emb = [0.0] * 1536  # example dimension for OpenAI embeddings
        embeddings.append({"text": seg["text"], "embedding": placeholder_emb})
    return embeddings


# Example usage (commented out):
# if __name__ == "__main__":
#     segs = [{"text":"The quick brown fox"},{"text":"jumps over"}]
#     print(json.dumps(transcript_embedding(segs), indent=2))
