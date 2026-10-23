from openai import OpenAI
import os
from typing import Dict

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL_NAME = "gpt-4o-mini"

def summarize_message(payload: Dict) -> str:
    prompt = f"Summarize the following message in one sentence:\n\n{payload}"
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50
    )
    
    return response.choices[0].message.content.strip()