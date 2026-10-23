import os

from openai import OpenAI

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


_DEFENSIVE_BLOCKLIST = {"password", "secret", "credit card", "ssn"}


def check_corpus_text(text: str) -> dict[str, object]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    flagged = any(result.flagged for result in moderation.results)
    lower = text.lower()
    sensitive_hits = sorted(term for term in _DEFENSIVE_BLOCKLIST if term in lower)
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": flagged or bool(sensitive_hits),
        "sensitive_hits": sensitive_hits,
    }
