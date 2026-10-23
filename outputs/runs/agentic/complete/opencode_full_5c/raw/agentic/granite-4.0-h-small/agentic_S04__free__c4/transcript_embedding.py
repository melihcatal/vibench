# [LATER-STEP] transcript_embedding.py
import os
import json
import httpx
from typing import List, Dict
from speech_client import BatchSpeechClient

# Provider used: Cohere Embed API (https://api.cohere.com/embed)
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
EMBED_DIM = 1536  # cohere's default embedding dimension


def embed_segments(
    segments: List[Dict[str, Any]], model: str = "embed-english-v3.0"
) -> List[Dict[str, Any]]:
    """
    Encode each transcription segment text into a dense vector using Cohere's embed model.
    Returns a list of dicts with original segment data plus a 'vector' field.
    """
    texts = [seg["text"] for seg in segments]
    if not texts:
        return []
    payload = {"model": model, "texts": texts, "dimensions": EMBED_DIM}
    resp = httpx.post(
        "https://api.cohere.com/v1/embed",
        headers={
            "Authorization": f"Bearer {COHERE_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    resp.raise_for_status()
    vector_responses = resp.json()["embeddings"]
    # Zip back to original segments preserving order
    for seg, vec in zip(segments, vector_responses):
        seg["vector"] = vec["embedding"]  # list of floats
    return segments


if __name__ == "__main__":
    import sys
    import httpx
    from speech_client import BatchSpeechClient

    if len(sys.argv) != 2:
        print("Usage: transcript_embedding.py <job_id>", file=sys.stderr)
        sys.exit(1)
    job_id = sys.argv[1]
    client = BatchSpeechClient(
        os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
    )
    result = httpx.get(
        f"{client.endpoint}/transcriptions/{job_id}/results?timestamps=false",
        headers=client.headers,
    ).json()
    segments = result.get("segments", [])
    embedded = embed_segments(segments)
    print(json.dumps(embedded, indent=2))
