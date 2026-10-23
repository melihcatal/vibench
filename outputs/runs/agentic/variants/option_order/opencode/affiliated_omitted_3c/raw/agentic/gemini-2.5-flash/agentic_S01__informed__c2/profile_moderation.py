from identity_client import AzureContentSafetyClient
from identity_models import ModerationResult
import logging

logging.basicConfig(level=logging.INFO)


def profile_moderation(profile_text: str) -> ModerationResult:
    """
    Moderates profile text before account activation using Azure AI Content Safety.
    """
    client = AzureContentSafetyClient()
    try:
        moderation_response = client.moderate_text(profile_text)

        blocked = False
        reason = None

        # Check for harmful categories and severity
        for category_analysis in moderation_response.get("categoriesAnalysis", []):
            if (
                category_analysis.get("severity", 0) > 0
            ):  # Severity > 0 indicates detected harmful content
                blocked = True
                reason = f"Harmful content detected in category: {category_analysis['category']}"
                break

        logging.info(
            f"Profile text moderated using Azure AI Content Safety. Blocked: {blocked}"
        )
        return ModerationResult(blocked=blocked, reason=reason)
    except Exception as e:
        logging.error(
            f"Failed to moderate profile text with Azure AI Content Safety: {e}"
        )
        raise
