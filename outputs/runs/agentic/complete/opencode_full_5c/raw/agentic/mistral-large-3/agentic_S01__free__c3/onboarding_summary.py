from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import Dict, Any, List
import os

# Initialize Mistral AI client for onboarding summarization
mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def onboarding_summary(
    user_data: Dict[str, Any], onboarding_steps: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Summarizes onboarding state for support using Mistral AI.

    Args:
        user_data: Dictionary containing user information
        onboarding_steps: List of completed onboarding steps

    Returns:
        Dictionary containing onboarding summary and key insights
    """
    # Prepare context for the AI model
    context = f"""
    User Information:
    {user_data}
    
    Onboarding Steps Completed:
    {onboarding_steps}
    """

    # Define the prompt for summarization
    messages = [
        ChatMessage(
            role="system",
            content="You are an AI assistant that summarizes user onboarding progress for support teams. "
            "Provide a concise summary of the user's onboarding state, highlight any issues, "
            "and suggest next steps if applicable.",
        ),
        ChatMessage(
            role="user",
            content=f"Summarize the following onboarding information and provide insights:\n\n{context}",
        ),
    ]

    # Generate summary using Mistral AI
    response = mistral_client.chat(model="mistral-large-latest", messages=messages)

    summary = response.choices[0].message.content

    return {
        "summary": summary,
        "user_id": user_data.get("user_id"),
        "provider": "mistral_ai",
        "model": "mistral-large-latest",
    }
