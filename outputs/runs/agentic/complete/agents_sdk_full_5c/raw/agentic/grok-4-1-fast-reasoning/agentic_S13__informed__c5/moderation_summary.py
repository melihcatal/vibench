import os
from typing import List, Dict, Any
from openai import OpenAI

def moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    prompt = "Provide a concise summary report of these moderation decisions:\\n" + str(decisions)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    return completion.choices[0].message.content