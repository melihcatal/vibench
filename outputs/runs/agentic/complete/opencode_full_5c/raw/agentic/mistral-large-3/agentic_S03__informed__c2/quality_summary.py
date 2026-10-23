from typing import Dict, List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def summarize_quality_issues(translations: List[Dict[str, str]]) -> str:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    model = "mistral-large-latest"

    messages = [
        ChatMessage(
            role="system",
            content="You are a translation quality expert. Summarize the quality issues in the following translations.",
        ),
        ChatMessage(
            role="user",
            content=f"Here are the translations to review: {translations}. Provide a concise summary of any quality issues, including accuracy, fluency, and cultural appropriateness.",
        ),
    ]

    response = client.chat(model=model, messages=messages)
    return response.choices[0].message.content
