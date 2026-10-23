import os
import json
from model_client import get_llm_client

def summarize_text(long_text, model_family="gpt-4", max_tokens=200):
    """Summarize long text using a hosted LLM."""
    client = get_llm_client(model_family)
    prompt = f"Summarize the following text in at most {max_tokens} words:\n\n{long_text}"
    response = client.chat_completion(prompt=prompt, max_tokens=max_tokens)
    return response["message"]["content"]
