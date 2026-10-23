import os
import json
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_message_processing(results: List[Dict[str, Any]]) -> str:
    text = json.dumps(results, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the message processing results:\n{text}",
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()
