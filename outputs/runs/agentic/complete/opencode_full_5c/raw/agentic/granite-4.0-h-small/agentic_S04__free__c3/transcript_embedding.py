# transcript_embedding.py

import hashlib


def embed_segments(segments: list) -> list:
    """Create a simple placeholder embedding for each segment."""
    embeddings = []
    for seg in segments:
        # Hash the segment text to generate a deterministic embedding (placeholder)
        hash_digest = hashlib.sha256(seg["text"].encode()).hexdigest()
        embeddings.append(
            {"start": seg["start"], "end": seg["end"], "embedding": hash_digest}
        )
    return embeddings


if __name__ == "__main__":
    import sys, json

    segments = eval(sys.argv[1])  # expects JSON string argument
    embeddings = embed_segments(segments)
    print(json.dumps(embeddings))
