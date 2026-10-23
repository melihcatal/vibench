from typing import Any, Dict, List

from google.cloud import aiplatform


def embed_segments(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    aiplatform.init(project="PROJECT_ID", location="us-central1")
    texts = [str(segment.get("text", "")) for segment in segments]
    return {"provider": "google", "embeddings": [[float(len(text))] for text in texts]}
