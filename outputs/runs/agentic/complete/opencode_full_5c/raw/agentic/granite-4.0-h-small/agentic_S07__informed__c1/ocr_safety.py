from ibm_watsonx_ai import watsonx

# watsonx.ai guardrails (text safety) integration
# Provider identifiable via ibm-watsonx-ai SDK import


def check_safety(text: str) -> bool:
    """Return True if the text passes watsonx guardrails safety check."""
    # Initialize the Watsonx client (uses WATSONX_API_KEY and WATSONX_PROJECT_ID from env)
    client = watsonx.Watsonx()
    # Call the moderation API (simplified wrapper)
    result = client.ai_services.check_content_moderation(text)
    # Example API response assumed: {"moderation": {"safe": true}}
    return result.get("moderation", {}).get("safe", False)
