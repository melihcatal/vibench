from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from typing import Dict, Optional
from .vision_models import ImageAnalysisSummary
import os


def image_summary(analysis_results: ImageAnalysisSummary) -> str:
    """Summarizes visual analysis results using Mistral Chat API."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable not set.")

    client = MistralClient(api_key=api_key)

    prompt = (
        "Summarize the following image analysis results in a concise paragraph:\n"
        f"Labels: {analysis_results.labels.labels if analysis_results.labels else 'None'}\n"
        f"Detected Text: {analysis_results.text.text if analysis_results.text else 'None'}\n"
        f"Description: {analysis_results.description.description if analysis_results.description else 'None'}\n"
        f"Safety Ratings - Adult: {analysis_results.safety_ratings.adult if analysis_results.safety_ratings else 'None'}, "
        f"Violence: {analysis_results.safety_ratings.violence if analysis_results.safety_ratings else 'None'}, "
        f"Racy: {analysis_results.safety_ratings.racy if analysis_results.safety_ratings else 'None'}"
    )

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model="mistral-large-latest", messages=messages)

    return response.choices[0].message.content
