from __future__ import annotations

from document_client import (
    GOOGLE_AI_MODERATION_URL,
    build_google_query_params,
    build_google_vision_headers,
    post_json,
)
from document_models import SafetyResult


def check_ocr_text_safety(text: str) -> SafetyResult:
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Classify whether this OCR document text contains unsafe content and return concise reasoning: {text}"
                    }
                ]
            }
        ],
        "generationConfig": {"temperature": 0.0},
        "safetySettings": [
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
    }
    response_json = post_json(
        GOOGLE_AI_MODERATION_URL,
        payload,
        headers=build_google_vision_headers(),
        params=build_google_query_params("GOOGLE_API_KEY"),
    )
    prompt_feedback = response_json.get("promptFeedback", {})
    block_reason = prompt_feedback.get("blockReason")
    safety_ratings = prompt_feedback.get("safetyRatings", [])
    categories = {
        rating.get("category", "unknown"): rating for rating in safety_ratings
    }
    return SafetyResult(
        provider="google-gemini",
        flagged=bool(block_reason),
        categories=categories,
        raw_response=response_json,
    )
