import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from vision_models import VisualAnalysis

client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))

def image_summary(analysis: VisualAnalysis) -> str:
    prompt = f"""Summarize the image analysis results concisely.

Labels: {analysis.get('labels', {})}
Description: {analysis.get('description', {}).get('description', '')}
Texts: {analysis.get('texts', {})}
Safety: {analysis.get('safety', {})}

Provide a short overall summary."""
    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model="mistral-large-latest", messages=messages)
    return response.choices[0].message.content