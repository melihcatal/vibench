from typing import Iterable, List

from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, SafetySetting

from speech_models import normalize_transcript


def check_live_transcript_safety(chunks: Iterable[str]) -> List[bool]:
    model = GenerativeModel("gemini-1.5-flash")
    safety = [SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_MEDIUM_AND_ABOVE")]
    results: List[bool] = []
    for chunk in chunks:
        text = normalize_transcript(chunk)
        if not text:
            continue
        response = model.generate_content(text, safety_settings=safety)
        results.append(bool(getattr(response, "text", "")))
    return results
