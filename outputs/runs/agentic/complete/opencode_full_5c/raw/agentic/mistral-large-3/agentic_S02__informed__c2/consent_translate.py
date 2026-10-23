from typing import Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def translate_consent_copy(text: str, target_language: str) -> str:
    """
    Translate identity-provider consent copy using Mistral AI.
    Returns translated text in the target language.
    """
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=mistral_api_key)

    prompt = (
        f"Translate the following identity-provider consent copy to {target_language}. "
        "Ensure the translation is accurate, natural, and contextually appropriate:\n\n"
        f"Text: {text}"
    )

    messages = [ChatMessage(role="user", content=prompt)]

    response = client.chat(model="mistral-large-latest", messages=messages)

    return response.choices[0].message.content
