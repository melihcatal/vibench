import os
import json
from typing import List, Dict, Any
from openai import OpenAI


def summarize_records(records: List[Dict[str, Any]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = OpenAI(api_key=api_key)
    prompt = f"""Provide a concise summary of these document records:

{json.dumps(records, default=str, indent=2)}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000,
    )
    return response.choices[0].message.content.strip()
