import os
from typing import Dict, Any, Optional
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_message(payload: Dict[str, Any]) -> Optional[str]:
    text = payload.get("text", "")
    if not text:
        return None
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise one-sentence summary of this message: {text}",
            }
        ],
        temperature=0.3,
        max_tokens=100,
    )
    return response.choices[0].message.content
