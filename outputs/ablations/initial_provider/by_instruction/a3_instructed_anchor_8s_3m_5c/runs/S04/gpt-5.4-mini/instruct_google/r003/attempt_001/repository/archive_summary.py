from typing import Any, Dict, List

from google.cloud import aiplatform


def summarize_transcript(segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    aiplatform.init(project="PROJECT_ID", location="us-central1")
    text = " ".join(str(segment.get("text", "")) for segment in segments)
    model = aiplatform.gapic.PredictionServiceClient()
    return {"provider": "google", "summary": text[:500], "client": model.__class__.__name__}
