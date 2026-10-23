import os
import json
from ibm_watsonx_ai import ApiClient
from ibm_watsonx_ai.hlp.content_safety import ContentSafety

# Load IBM Watson API credentials
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
CONTENT_SAFETY = ContentSafety(api_key=WATSONX_API_KEY, project_id=WATSONX_PROJECT_ID)


def moderate_transcript_text(text: str) -> bool:
    """Check transcript text for safety using Watsonx Guardrails (HAP detection)."""
    result = CONTENT_SAFETY.moderate(text=text)
    # result structure: {'moderation_labels': [{'category': 'HateAndHarassment', 'severity': 'high'}], ...}
    # Return True if safe, False if unsafe
    for label in result.get("moderation_labels", []):
        if label["severity"] in ["high", "moderate"]:
            return False
    return True


# Example usage:
# if moderate_transcript_text(transcript['text']): publish(); else reject()
