import openai
import os
import json
from typing import List, Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderation_summary(decisions: List[Dict[str, Any]]) -> str:
    """
    Summarize moderation decisions using OpenAI GPT-4o-mini.
    """
    prompt = f"""
Provide a concise summary of these moderation decisions:
{json.dumps(decisions, indent=2)}
Include: total items, allowed/blocked counts, top violation categories, any patterns.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a moderation analyst."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()
