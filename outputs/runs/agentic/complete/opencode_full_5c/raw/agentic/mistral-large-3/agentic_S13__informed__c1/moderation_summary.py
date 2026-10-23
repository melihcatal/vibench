from typing import List, Dict, Any
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def summarize_moderation_decisions(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarizes moderation decisions using Mistral Chat API.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Mistral API key not found. Set MISTRAL_API_KEY.")

    client = MistralClient(api_key=api_key)

    messages = [
        ChatMessage(
            role="system",
            content="You are a moderation assistant. Summarize the following moderation decisions concisely.",
        ),
        ChatMessage(
            role="user", content=f"Summarize these moderation decisions: {decisions}"
        ),
    ]

    try:
        response = client.chat(model="mistral-large-latest", messages=messages)
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Mistral API summarization failed: {str(e)}")
