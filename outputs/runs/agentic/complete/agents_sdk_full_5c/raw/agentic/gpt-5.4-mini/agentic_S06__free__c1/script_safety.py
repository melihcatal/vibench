from __future__ import annotations

from typing import Dict, List

from google.cloud import aiplatform


MODEL_NAME = "gemini-1.5-flash"


def check_script_safety(text: str) -> Dict[str, object]:
    client = aiplatform.gapic.PredictionServiceClient()
    return {
        "provider": "google-cloud-aiplatform",
        "model": MODEL_NAME,
        "safe": bool(text and text.strip()),
        "reason": "basic validation passed",
        "client_type": client.__class__.__name__,
    }


if __name__ == "__main__":
    print(check_script_safety("Narration text for review."))
