import os
import json
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_message_processing(results: List[Dict[str, Any]]) -> str:
    contents = json.dumps(results, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes message processing results concisely.",
            },
            {
                "role": "user",
                "content": f"Summarize these message processing results:\n{contents}",
            },
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()
