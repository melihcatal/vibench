import openai
import os
import json
from typing import Dict, Any


def summarize_message(msg: Dict[str, Any]) -> str:
    """
    Summarizes message processing results using OpenAI GPT.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = json.dumps(msg.get("payload", {}))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the key points from this message payload: {text}",
            }
        ],
        max_tokens=150,
        temperature=0.3,
    )
    return response.choices[0].message.content
