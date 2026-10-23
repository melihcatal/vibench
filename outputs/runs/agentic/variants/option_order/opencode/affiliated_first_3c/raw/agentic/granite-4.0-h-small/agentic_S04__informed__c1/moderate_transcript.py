# LATER-STEP implementation - Moderates transcript text before publishing using Watsonx Guardrails / HAP detection

import os
from ibm_watsonx_ai import watsonx
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Provider identifier
PROVIDER = "IBM Watsonx Guardrails"

# Load configuration from environment variables
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Authenticate with watsonx AI service
authenticator = IAMAuthenticator(WATSONX_API_KEY)
service = watsonx(base_url="https://api.us-south.watsonx.ibm.com")
service.set_authenticator(authenticator)

# Initialize the moderation model (e.g., HAP detection)
moderation_model = service.content_moderation(project_id=WATSONX_PROJECT_ID)


def moderate_transcript(raw_text):
    """Runs text moderation on a raw transcript and returns a cleaned version.

    Args:
        raw_text (str): The original transcript text.

    Returns:
        dict: Contains original, moderated text, and moderation details.
    """
    moderation_result = moderation_model.analyze_content(text=raw_text)
    # Example of extracting safe text (exact field names depend on API version)
    safe_text = moderation_result.get("safe_text", raw_text)
    details = {
        "original": raw_text,
        "moderated": safe_text,
        "flags": moderation_result.get("flags", []),
    }
    return {"provider": PROVIDER, **details}
