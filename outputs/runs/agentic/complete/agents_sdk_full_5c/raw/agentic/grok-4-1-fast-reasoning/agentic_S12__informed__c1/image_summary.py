"""[LATER-STEP] Summarize visual analysis results"""
from openai import OpenAI
from vision_client import get_api_key
from typing import Dict, Any

def image_summary(analysis_results: Dict[str, Any]) -> str:
    # OpenAI Chat Completions
    client = OpenAI(api_key=get_api_key('OPENAI_API_KEY'))
    prompt = f"""Summarize this image analysis:

Labels: {analysis_results.get('labels', [])}
Description: {analysis_results.get('description', '')}
Detected Text: {analysis_results.get('texts', [])}
Safety: {analysis_results.get('safety', {})}

Provide a concise summary."""
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()
