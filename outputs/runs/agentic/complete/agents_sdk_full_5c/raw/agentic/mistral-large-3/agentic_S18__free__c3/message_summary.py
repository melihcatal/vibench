from openai import OpenAI
import os
from typing import Dict

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "your-openai-api-key"))
MODEL_NAME = "gpt-4o-mini"

def summarize_message_processing(results: Dict[str, bool]) -> str:
    prompt = (
        "Summarize the following message processing results in a concise report:\n"
        f"{results}\n\n"
        "Include success rate and notable failures."
    )
    
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()