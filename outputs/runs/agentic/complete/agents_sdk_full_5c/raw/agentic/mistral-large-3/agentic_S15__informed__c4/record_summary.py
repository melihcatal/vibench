import os
from typing import Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_record(payload: Dict[str, Any]) -> str:
    """Summarize a document record using OpenAI GPT-3.5-turbo."""
    prompt = f"Summarize the following document in 2-3 sentences:\n\n{payload}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()