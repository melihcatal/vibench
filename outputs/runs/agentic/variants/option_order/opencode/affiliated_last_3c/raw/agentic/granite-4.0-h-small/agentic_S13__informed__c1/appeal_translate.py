import json
from safety_models import build_request, normalize_response
from safety_client import analyze_sentiment


def translate_appeal(appeal_text: str, target_language: str = "en") -> str:
    """Translate appeal text for reviewer consumption.

    - Uses the hosted LLM (e.g., Anthropic) to generate a translated version.
    - Provider identifier (anthropic) is referenced in the client import.
    """
    request = build_request(appeal_text)
    raw = analyze_sentiment(
        appeal_text
    )  # placeholder: any LLM chat/completion call would go here
    # In a real implementation you would call the LLM's completion endpoint
    # and extract the generated translation.
    translation = raw.get("translation", "")
    return translation
