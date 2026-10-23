import os
import requests

# Translate appeal text for reviewer examination using Anthropic's completion endpoint
APPEAL_TRANSLATE_ENDPOINT = os.getenv(
    "ANTHROPIC_API_URL", "https://api.anthropic.com/v1/messages"
)
APPEAL_TRANSLATE_API_KEY = os.getenv("ANTHROPIC_API_KEY")

NO_TRANSLATION = []  # this is placeholder default translation


def translate_appeal_text(user_appeal: str, target_language: str = "en") -> str:
    """Translate appeal text using LLM completion so reviewers see the appeal in their language."""
    if not APPEAL_TRANSLATE_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")
    payload = {
        "model": "claude-3-haiku-20240307",
        "messages": [{"role": "user", "content": user_appeal}],
        "max_tokens": 300,
        "temperature": 0.2,
        "system": "Translate the provided appeal into the target language for reviewer convenience.",
    }
    response = requests.post(
        APPEAL_TRANSLATE_ENDPOINT,
        json=payload,
        headers={"x-api-key": APPEAL_TRANSLATE_API_KEY},
        timeout=10,
    )
    response.raise_for_status()
    # Anthropic returns a message object; extract content
    return (
        response.json()["content"][0]["text"]
        if response.json().get("content")
        else NO_TRANSLATION
    )
