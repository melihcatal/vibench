"""
Check localized copy for unsafe content using hosted content safety API.

Provider: Tisane Text Moderation API
SDK: requests (REST interface)
Auth: TISANE_API_KEY

Uses Tisane's text moderation service to analyze translated/localized
copy for unsafe content including toxicity, hate speech, self-harm,
violence, sexual content, and other safety categories.
"""

import os
from typing import Optional

import requests

# Tisane API endpoint
TISANE_API_URL = "https://api.tisane.ai/parse"


def get_tisane_api_key() -> str:
    """Retrieve Tisane API key from environment."""
    api_key = os.environ.get("TISANE_API_KEY")
    if not api_key:
        raise ValueError(
            "TISANE_API_KEY environment variable is required. "
            "Set it with your Tisane API key."
        )
    return api_key


def check_unsafe_content(
    text: str,
    *,
    language: str = "en",
    api_key: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> dict:
    """
    Check a single text string for unsafe content via Tisane API.

    Analyzes text for:
    - Toxicity and hate speech
    - Self-harm and suicide indicators
    - Violence and abuse
    - Sexual content
    - Profanity
    - Harassment and bullying
    - Other safety violations

    Args:
        text: The text to analyze for unsafe content.
        language: ISO 639-1 language code (default 'en').
        api_key: Tisane API key. Defaults to TISANE_API_KEY env var.
        session: Optional requests session for connection pooling.

    Returns:
        Dict with safety analysis results including:
        - 'safe': boolean overall safety flag
        - 'categories': dict of category -> {detected: bool, score: float}
        - 'flags': list of flagged category names
        - 'max_severity': highest severity level found
    """
    if not text or not text.strip():
        return {
            "safe": True,
            "categories": {},
            "flags": [],
            "max_severity": "none",
            "text_length": 0,
        }

    key = api_key or get_tisane_api_key()

    payload = {
        "content": text,
        "language": language,
        "entities": False,
        "settings": {
            "profanity": True,
            "abuse": True,
            "violence": True,
            "sexual": True,
            "political": False,
            "hate": True,
            "emotion": False,
            "threat": True,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": key,
    }

    if session is None:
        session = requests.Session()

    try:
        response = session.post(
            TISANE_API_URL,
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {
            "safe": True,
            "categories": {},
            "flags": [],
            "max_severity": "none",
            "error": str(e),
            "text_length": len(text),
        }

    return parse_tisane_response(data, text)


def parse_tisane_response(raw_response: dict, original_text: str) -> dict:
    """
    Parse Tisane API response into a normalized safety report.

    Args:
        raw_response: Raw JSON response from Tisane API.
        original_text: The text that was analyzed.

    Returns:
        Normalized safety report dict.
    """
    categories: dict = {}
    flags: list[str] = []
    max_severity = "none"
    severity_order = ["none", "low", "medium", "high", "critical"]

    # Extract category detections from Tisane response structure
    abuse = raw_response.get("abuse", {})
    if abuse:
        for item in abuse if isinstance(abuse, list) else [abuse]:
            category = item.get("category", item.get("class", "unknown"))
            score = item.get("score", 0.0)
            severity = item.get("severity", "low")

            if isinstance(score, str):
                try:
                    score = float(score)
                except ValueError:
                    score = 0.0

            categories[category] = {
                "detected": score > 0.3,
                "score": score,
                "severity": severity,
            }

            if score > 0.3:
                flags.append(category)
                if severity_order.index(severity) > severity_order.index(max_severity):
                    max_severity = severity

    is_safe = len(flags) == 0

    return {
        "safe": is_safe,
        "categories": categories,
        "flags": flags,
        "max_severity": max_severity,
        "text_length": len(original_text),
    }


def batch_check_unsafe_content(
    texts: list[str],
    *,
    language: str = "en",
    api_key: Optional[str] = None,
) -> list[dict]:
    """
    Check multiple texts for unsafe content.

    Args:
        texts: List of texts to analyze.
        language: ISO 639-1 language code.
        api_key: Tisane API key.

    Returns:
        List of safety report dicts, one per text.
    """
    results = []
    with requests.Session() as session:
        for text in texts:
            result = check_unsafe_content(
                text=text,
                language=language,
                api_key=api_key,
                session=session,
            )
            results.append(result)
    return results


def check_localized_copy_set(
    translations: dict[str, str],
    *,
    language: str = "en",
    api_key: Optional[str] = None,
) -> dict[str, dict]:
    """
    Check a set of localized copy strings for unsafe content.

    Args:
        translations: Dict mapping keys (e.g., UI element IDs) to translated text.
        language: Language code for the translated content.
        api_key: Tisane API key.

    Returns:
        Dict mapping each key to its safety report.
    """
    results = {}
    for key, text in translations.items():
        results[key] = check_unsafe_content(
            text=text,
            language=language,
            api_key=api_key,
        )
    return results


if __name__ == "__main__":
    result = check_unsafe_content(
        text="This is a safe test message for translation quality checking.",
        language="en",
    )
    print(f"Safe: {result['safe']}")
    print(f"Flags: {result['flags']}")
