import os
from typing import Dict, Any
from anthropic import Anthropic

def summarize_transcript(transcript_text: str, model_name: str = "claude-3-opus-20240229") -> str:
    """
    Summarizes the provided transcript text using Anthropic's Claude model.
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    messages = [
        {"role": "user", "content": f"Please provide a concise summary of the following meeting transcript:\n\n{transcript_text}"}
    ]
    
    response = client.messages.create(
        model=model_name,
        max_tokens=500,
        messages=messages
    )
    
    return response.content[0].text
