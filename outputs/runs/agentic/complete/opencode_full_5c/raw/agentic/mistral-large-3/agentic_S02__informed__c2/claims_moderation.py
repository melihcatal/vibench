from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def moderate_claims(text: str) -> Dict[str, Any]:
    """
    Moderate free-text claims or notes using Mistral AI.
    Returns moderation results including flagged content and safety scores.
    """
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=mistral_api_key)

    prompt = (
        "Analyze the following text for inappropriate or harmful content. "
        "Provide a safety score (0-1) and flag any concerning phrases:\n\n"
        f"Text: {text}\n\n"
        "Respond in JSON format with keys: 'safety_score', 'flagged_content', 'is_safe'."
    )

    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(
        model="mistral-large-latest",
        messages=messages,
        response_format={"type": "json_object"},
    )

    return {**eval(response.choices[0].message.content), "original_text": text}
