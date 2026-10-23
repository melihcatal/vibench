import os
import json
from typing import Dict, Any
from anthropic import Anthropic


def summarize_embedding_job(job_results: Dict[str, Any]) -> str:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required.")
    client = Anthropic(api_key=api_key)
    prompt = f"""Summarize this embedding job in 2-3 sentences, highlighting key metrics, model used, and any issues:
{json.dumps(job_results, indent=2)}"""
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
