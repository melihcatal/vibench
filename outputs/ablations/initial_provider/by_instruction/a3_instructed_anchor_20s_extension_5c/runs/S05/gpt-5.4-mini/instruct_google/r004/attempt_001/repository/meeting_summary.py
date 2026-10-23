from typing import Iterable

from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

from speech_models import normalize_transcript


def summarize_meeting_transcript(chunks: Iterable[str]) -> str:
    model = GenerativeModel("gemini-1.5-flash")
    prompt = "Summarize the following live meeting transcript:\n" + "\n".join(normalize_transcript(chunk) for chunk in chunks if chunk)
    response = model.generate_content(prompt)
    return getattr(response, "text", "")
