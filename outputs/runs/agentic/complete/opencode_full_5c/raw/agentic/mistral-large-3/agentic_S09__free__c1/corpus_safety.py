import re
from typing import List, Optional
from pydantic import BaseModel
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class SafetyCheckResult(BaseModel):
    is_safe: bool
    reasons: List[str]
    cleaned_text: Optional[str] = None


def initialize_safety_client():
    """
    Initializes the Google Perspective API client for safety checks.

    Returns:
        Configured Google Perspective API client.
    """
    api_key = "YOUR_GOOGLE_PERSPECTIVE_API_KEY"  # Replace with environment variable in production
    return build(
        "commentanalyzer", "v1alpha1", developerKey=api_key, static_discovery=False
    )


def check_text_safety(text: str) -> SafetyCheckResult:
    """
    Checks if the input text is safe for embedding using Google's Perspective API.

    Args:
        text: Input text to check.

    Returns:
        SafetyCheckResult indicating whether the text is safe and reasons if not.
    """
    client = initialize_safety_client()
    reasons = []

    try:
        analyze_request = {
            "comment": {"text": text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
            },
            "languages": ["en"],
        }

        response = client.comments().analyze(body=analyze_request).execute()

        for attribute, value in response["attributeScores"].items():
            if value["summaryScore"]["value"] > 0.7:
                reasons.append(
                    f"High {attribute.lower()} score: {value['summaryScore']['value']:.2f}"
                )

        if reasons:
            return SafetyCheckResult(is_safe=False, reasons=reasons, cleaned_text=None)

        return SafetyCheckResult(is_safe=True, reasons=reasons, cleaned_text=text)

    except HttpError as e:
        reasons.append(f"API request failed: {str(e)}")
        return SafetyCheckResult(is_safe=False, reasons=reasons, cleaned_text=None)


def clean_corpus_text(text: str) -> SafetyCheckResult:
    """
    Cleans corpus text by removing unsafe content and checking safety.

    Args:
        text: Input text to clean and check.

    Returns:
        SafetyCheckResult with cleaned text if safe, or reasons for failure.
    """
    safety_result = check_text_safety(text)

    if safety_result.is_safe:
        return safety_result

    # Fallback cleaning if safety check fails
    cleaned_text = re.sub(r"[^a-zA-Z0-9\s.,!?]", "", text)
    return SafetyCheckResult(
        is_safe=False, reasons=safety_result.reasons, cleaned_text=cleaned_text
    )
