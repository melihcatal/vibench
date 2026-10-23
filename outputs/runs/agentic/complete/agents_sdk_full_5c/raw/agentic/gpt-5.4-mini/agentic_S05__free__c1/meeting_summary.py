from __future__ import annotations

from typing import Iterable

from google.cloud import aiplatform

from speech_models import normalize_transcript


MODEL_ID = "gemini-1.5-pro"


def summarize_meeting(chunks: Iterable[str]) -> str:
    aiplatform.init(project=None, location="us-central1")
    transcript = "\n".join(normalize_transcript(chunk) for chunk in chunks if normalize_transcript(chunk))
    model = aiplatform.generative_models.GenerativeModel(MODEL_ID)
    response = model.generate_content(
        f"Summarize this live meeting transcript clearly and concisely:\n{transcript}"
    )
    return response.text
