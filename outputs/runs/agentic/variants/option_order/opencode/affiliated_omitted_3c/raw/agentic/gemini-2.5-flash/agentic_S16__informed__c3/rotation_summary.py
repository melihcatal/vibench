import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_rotation_status(rotation_log: str) -> str:
    """Summarizes secret rotation status using Mistral Chat API.

    Args:
        rotation_log: A string containing the rotation log or status to summarize.

    Returns:
        A summarized string of the rotation status.

    Raises:
        Exception: If the Mistral API key is not set or API call fails.
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable must be set.")

    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(
            role="user",
            content=f"Summarize the following secret rotation status or log concisely: {rotation_log}",
        )
    ]

    try:
        chat_response = client.chat(model="mistral-small", messages=messages)
        return chat_response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Mistral API call failed: {e}")
