import os
import json
from typing import Dict, Any
from openai import OpenAI


def summarize_embedding_job(job_results: Dict[str, Any]) -> str:
    """
    Summarizes embedding job results using OpenAI gpt-4o-mini.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = "gpt-4o-mini"
    prompt = f"""
    Provide a concise summary of the embedding job results:
    {json.dumps(job_results, indent=2)}
    """
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}], max_tokens=200
    )
    return response.choices[0].message.content.strip()
