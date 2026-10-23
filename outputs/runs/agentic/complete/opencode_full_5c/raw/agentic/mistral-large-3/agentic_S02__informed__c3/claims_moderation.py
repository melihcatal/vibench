from typing import Dict, Any
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Mistral Chat API for content moderation
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = "mistral-large-latest"


def claims_moderation(claims: Dict[str, Any]) -> Dict[str, Any]:
    """Moderate free-text claims using Mistral."""
    client = MistralClient(api_key=MISTRAL_API_KEY)

    prompt = (
        "Analyze the following user profile claims for inappropriate content. "
        "Flag any claims that violate content policies and suggest alternatives:\n\n"
        f"{claims}"
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model=MISTRAL_MODEL, messages=messages)

    # Parse response (simplified)
    moderation_result = {
        "is_flagged": "inappropriate" in response.choices[0].message.content.lower(),
        "flags": [],
        "suggestions": response.choices[0].message.content,
    }

    return moderation_result
