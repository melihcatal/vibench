import os
import anthropic
from typing import Dict, Any

def embedding_job_summary(job_results: Dict[str, Any]) -> str:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Provide a concise summary of the embedding job results:

{job_results}"""
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text