from __future__ import annotations

from safety_client import get_gemini_client, safety_model_name
from safety_models import ThresholdRequest, ThresholdResult, normalize_threshold_response


THRESHOLD_PROMPT = """Apply category thresholds to decide whether to allow text.\nReturn JSON with keys: allowed, threshold_hits, categories, explanation.\n"""


def safety_threshold(text: str, thresholds: dict[str, float]) -> ThresholdResult:
    request = ThresholdRequest(text=text, thresholds=thresholds)
    client = get_gemini_client()
    response = client.models.generate_content(  # google-genai SDK
        model=safety_model_name("threshold"),
        contents=[THRESHOLD_PROMPT, request.to_prompt()],
        generation_config={"temperature": 0},
    )
    return normalize_threshold_response(response)
