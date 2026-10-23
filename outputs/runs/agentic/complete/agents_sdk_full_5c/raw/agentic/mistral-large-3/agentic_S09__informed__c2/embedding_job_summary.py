import os
from typing import Dict, Any

from openai import OpenAI


def summarize_embedding_job(job_metadata: Dict[str, Any]) -> str:
    """Summarize embedding job results using OpenAI GPT-4."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Summarize the following embedding job results in a concise report:\n"
        f"Input texts: {job_metadata.get('input_count', 0)}\n"
        f"Embedding model: {job_metadata.get('model', 'unknown')}\n"
        f"Token usage: {job_metadata.get('token_usage', {})}\n"
        f"Processing time: {job_metadata.get('processing_time', 'unknown')} seconds\n"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()