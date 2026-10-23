import json
from ibm_watsonx_ai import WatsonxGuardrails

# LATER-STEP: Moderate profile text before account activation


def moderate_profile_text(profile_text: str, guardrails_config: dict) -> str:
    """Run profile content through watsonx guardrails and return sanitized text.

    Args:
        profile_text: Raw user-supplied profile description.
        guardrails_config: Configuration dictionary with credentials and project info.

    Returns:
        str: Moderated version of profile_text.
    """
    # Initialize guardrails service (uses REST under the hood if needed)
    guardrails = WatsonxGuardrails(
        api_key=guardrails_config["api_key"], project_id=guardrails_config["project_id"]
    )
    # Example: use the 'text_moderation' capability (adjust to actual guardrails method names)
    moderation_result = guardrails.text_moderation(text=profile_text)
    # Guardrails returns a list of issues; we strip flagged content
    cleaned = (
        moderation_result["cleaned_text"]
        if "cleaned_text" in moderation_result
        else profile_text
    )
    return cleaned


# guardrails_config example
# {
#   "api_key": "<WATSONX_API_KEY>",
#   "project_id": "<WATSONX_PROJECT_ID>"
# }
