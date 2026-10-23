from anthropic import Anthropic
import os
from typing import Dict, Any

def image_summary(analysis_results: Dict[str, Any]) -> str:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    prompt = f"""Summarize the key visual elements, objects, text, and any safety concerns from this image analysis:

Labels: {analysis_results.get('labels', [])}
Description: {analysis_results.get('description', '')}
Text: {analysis_results.get('text', '')}
Safety: {analysis_results.get('safety', {})}

Provide a concise 2-3 sentence summary."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()