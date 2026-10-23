import re

# Check secret labels/notes for unsafe content
# Uses watsonx.ai guardrails (content safety) as an example
import os

from ibm_watsonx_ai.services import WatsonXaiContentSafety
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

authenticator = IAMAuthenticator(WATSONX_API_KEY)
content_service = WatsonXaiContentSafety(
    authenticator=authenticator, project_id=WATSONX_PROJECT_ID
)


def check_label_safety(label: str) -> bool:
    """Flag a secret label as unsafe if it contains disallowed terms.",
    Returns True when safe, False otherwise.
    """
    response = content_service.analyze_content(text=label)
    # The service returns a probability for each risk category; we'll use a simple rule:
    # if any category exceeds 0.8 confidence, consider it unsafe.
    risks = response.get("categories", [])
    for cat in risks:
        if (
            cat["label"] in ["profanity", "hate", "self harm"]
            and cat["confidence"] > 0.8
        ):
            return False
    return True


if __name__ == "__main__":
    test_label = os.getenv("TEST_SECRET_LABEL", "This is safe.")
    print("Label safe?", check_label_safety(test_label))
