import os
import requests
from typing import List, Dict, Any, Optional

from speech_models import SegmentEmbedding

OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return api_key


def create_embeddings(
    texts: List[str],
    model: str = OPENAI_EMBEDDING_MODEL,
) -> List[List[float]]:
    api_key = get_openai_api_key()

    response = requests.post(
        OPENAI_EMBEDDINGS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "input": texts,
            "model": model,
        },
    )
    response.raise_for_status()
    data = response.json()

    embeddings = []
    for item in data["data"]:
        embeddings.append(item["embedding"])

    return embeddings


def embed_transcript_segments(
    transcript_data: Dict[str, Any],
    segment_key: str = "segments",
) -> Dict[str, Any]:
    segments = transcript_data.get(segment_key, [])
    if not segments:
        text = transcript_data.get("text", "")
        if text:
            segments = [{"text": text, "start": 0, "end": 0}]

    texts = [seg.get("text", "") for seg in segments if seg.get("text")]
    if not texts:
        return {
            "provider": "OpenAI",
            "model": OPENAI_EMBEDDING_MODEL,
            "embeddings": [],
            "total_segments": 0,
        }

    embeddings = create_embeddings(texts, model=OPENAI_EMBEDDING_MODEL)

    embedded_segments = []
    for i, seg in enumerate(segments):
        if i < len(embeddings):
            embedded_segments.append(
                SegmentEmbedding(
                    text=seg.get("text", ""),
                    embedding=embeddings[i],
                    start=seg.get("start", 0),
                    end=seg.get("end", 0),
                    speaker=seg.get("speaker"),
                )
            )

    return {
        "provider": "OpenAI",
        "model": OPENAI_EMBEDDING_MODEL,
        "total_segments": len(embedded_segments),
        "embedding_dimension": len(embeddings[0]) if embeddings else 0,
        "embeddings": [
            {
                "text": e.text,
                "start": e.start,
                "end": e.end,
                "speaker": e.speaker,
                "vector": e.embedding,
            }
            for e in embedded_segments
        ],
    }


def transcript_embedding(transcript_data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
    return embed_transcript_segments(transcript_data, **kwargs)


if __name__ == "__main__":
    import sys

    text = sys.argv[1] if len(sys.argv) > 1 else ""
    if not text:
        print("Usage: python transcript_embedding.py <text>")
        sys.exit(1)

    result = embed_transcript_segments({"text": text})
    print(result)
