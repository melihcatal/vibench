import os
from typing import List, Dict

from model_client import create_chat_completion
from model_models import extract_content, ChatMessages

def summarize_text(text: str) -> str:
    messages: ChatMessages = [
        {"role": "system", "content": "You are a concise summarizer. Provide a brief summary."},
        {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
    ]
    response = create_chat_completion(messages)
    return extract_content(response)