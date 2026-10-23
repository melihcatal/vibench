from identity_client import AnthropicClient
from identity_models import OnboardingSummary
import logging

logging.basicConfig(level=logging.INFO)

def onboarding_summary(onboarding_state_text: str) -> OnboardingSummary:
    """
    Summarizes onboarding state for support using Anthropic Messages API.
    """
    client = AnthropicClient()
    system_prompt = "You are a helpful assistant that summarizes user onboarding states. Provide a concise summary of the provided onboarding state information."
    user_message = f"Please summarize the following user onboarding state:

{onboarding_state_text}"

    try:
        response_data = client.create_message(system_prompt, user_message)
        summary_text = ""
        for content_block in response_data.get("content", []):
            if content_block.get("type") == "text":
                summary_text += content_block.get("text", "")
        
        logging.info(f"Onboarding state summarized using Anthropic model: {client.model}")
        return OnboardingSummary(summary_text=summary_text.strip())
    except Exception as e:
        logging.error(f"Failed to summarize onboarding state with Anthropic: {e}")
        raise