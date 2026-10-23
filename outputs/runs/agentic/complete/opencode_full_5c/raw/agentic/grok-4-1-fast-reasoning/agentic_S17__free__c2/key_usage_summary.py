import openai
import os
import json
from typing import List, Dict, Any


def summarize_key_usage(events: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    events_str = json.dumps(events, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a security auditor specializing in cryptographic key management. Provide a concise summary of key usage patterns, notable events, potential issues, and recommendations.",
            },
            {
                "role": "user",
                "content": f"Analyze and summarize these crypto events:\\n\\n{events_str}",
            },
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content
