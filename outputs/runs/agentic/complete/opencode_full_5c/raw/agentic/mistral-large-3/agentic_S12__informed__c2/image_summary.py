from typing import Dict, List
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os


def summarize_visual_analysis(
    labels: List[dict],
    description: str,
    text_detections: List[dict],
    safety_scores: Dict[str, str],
) -> str:
    """
    Summarizes visual analysis results using Mistral's hosted LLM.
    """
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    prompt = f"""
    Summarize the following visual analysis results for an image:
    
    Labels detected: {labels}
    Description: {description}
    Text detected: {text_detections}
    Safety scores: {safety_scores}
    
    Provide a concise summary in 2-3 sentences.
    """

    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content
