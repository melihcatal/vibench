import os
import json
from mistralai import Mistral
from mistralai.models.chat_completion import ChatMessage
from .vision_models import VisionResult

def image_summary(analysis: VisionResult) -> str:
    client = Mistral(api_key=os.getenv('MISTRAL_API_KEY'))
    prompt = f"""Provide a concise summary of the image based on this analysis:

Labels: {json.dumps(analysis.get('labels', []))}
Caption: {json.dumps(analysis.get('caption', {}))}
Detected Text: {json.dumps(analysis.get('detections', []))}
Safety: {json.dumps(analysis.get('moderation_labels', []))}

Summary:"""
    messages = [ChatMessage(role='user', content=prompt)]
    response = client.chat(model='mistral-large-latest', messages=messages)
    return response.choices[0].message.content.strip()