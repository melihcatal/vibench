import os
import sys
import boto3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import ModerateTextRequest, ModerateTextResponse


def profile_moderation(request: ModerateTextRequest) -> ModerateTextResponse:
    identity_client = IdentityClient()
    comprehend_client = identity_client.get_comprehend_client()

    try:
        # Amazon Comprehend can detect PII and toxicity. For general content moderation,
        # a combination of features might be used. Here we'll use PII detection as an example
        # and simulate a 'toxicity' check for demonstration.

        # PII Detection
        pii_response = comprehend_client.detect_pii_entities(
            Text=request.text,
            LanguageCode="en",  # Assuming English for moderation
        )

        is_safe = True
        reasons = []

        if pii_response["Entities"]:
            is_safe = False
            reasons.append("Contains Personally Identifiable Information (PII).")

        # For more comprehensive moderation (e.g., toxicity), a custom model or
        # a different Comprehend feature like 'DetectSentiment' or 'DetectDominantLanguage'
        # followed by rule-based checks would be needed. For this example, let's
        # add a simple keyword check to simulate a basic 'toxicity' aspect.

        toxic_keywords = ["hate", "kill", "attack", "abuse"]
        if any(keyword in request.text.lower() for keyword in toxic_keywords):
            is_safe = False
            reasons.append("Contains potentially toxic language (keyword match).")

        if not reasons:
            reasons.append("No immediate moderation flags detected.")

        return ModerateTextResponse(is_safe=is_safe, reasons=reasons)
    except Exception as e:
        return ModerateTextResponse(
            is_safe=False, reasons=[f"Moderation failed: {str(e)}"]
        )
