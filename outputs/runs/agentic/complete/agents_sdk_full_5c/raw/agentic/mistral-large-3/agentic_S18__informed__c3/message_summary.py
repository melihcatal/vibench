# Summarize message processing results using Mistral Chat API
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def summarize_message(message_data: dict) -> str:
    """Summarize message content using Mistral's mistral-tiny model."""
    api_key = os.getenv("MISTRAL_API_KEY")
    client = MistralClient(api_key=api_key)
    
    prompt = f"Summarize the following message in one concise sentence:\n\n{message_data}"
    
    chat_response = client.chat(
        model="mistral-tiny",
        messages=[ChatMessage(role="user", content=prompt)]
    )
    return chat_response.choices[0].message.content