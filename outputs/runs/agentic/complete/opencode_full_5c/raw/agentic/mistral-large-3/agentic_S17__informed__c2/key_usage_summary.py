import os
from typing import List, Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def key_usage_summary(crypto_events: List[Dict[str, Any]], api_key: str = None) -> dict:
    """
    Summarizes key usage and crypto events using Mistral's chat API.

    Args:
        crypto_events: List of crypto events to summarize.
        api_key: Mistral API key. Defaults to MISTRAL_API_KEY env var.

    Returns:
        Dictionary containing summary, model, provider, and success status.
    """
    api_key = api_key or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        return {
            "error": "Mistral API key not provided",
            "provider": "mistral",
            "success": False,
        }

    client = MistralClient(api_key=api_key)

    try:
        events_text = "\n".join([str(event) for event in crypto_events])
        prompt = f"Summarize the following crypto events in a concise manner:\n\n{events_text}"

        messages = [ChatMessage(role="user", content=prompt)]
        response = client.chat(model="mistral-large-latest", messages=messages)

        return {
            "summary": response.choices[0].message.content,
            "model": "mistral-large-latest",
            "provider": "mistral",
            "success": True,
        }
    except Exception as e:
        return {"error": str(e), "provider": "mistral", "success": False}
