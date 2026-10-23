import os
from typing import Dict, List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from .vision_models import (
    LabelDetectionResponse,
    ImageDescriptionResponse,
    TextDetectionResponse,
    SafetyScoreResponse,
)


def image_summary(
    labels: LabelDetectionResponse,
    description: ImageDescriptionResponse,
    texts: TextDetectionResponse,
    api_key: str = None,
) -> str:
    """
    Summarizes visual analysis results using Mistral's chat API.
    """
    api_key = api_key or os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set.")

    client = MistralClient(api_key=api_key)

    prompt = (
        f"Summarize the following visual analysis results for an image:\n"
        f"- Description: {description.description}\n"
        f"- Detected Labels: {', '.join(labels.labels)}\n"
        f"- Detected Text: {', '.join(texts.texts) if texts.texts else 'None'}\n"
        f"Provide a concise summary in 2-3 sentences."
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model="mistral-large-latest", messages=messages)

    if not response.choices:
        raise RuntimeError("Failed to generate summary.")

    return response.choices[0].message.content
