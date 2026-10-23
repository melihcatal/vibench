import os
from typing import Dict, Any
import openai


def summarize_document(document: Dict[str, Any]) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    fields_text = "\n".join(f"{k}: {v}" for k, v in document.get("fields", {}).items())
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Summarize the following document fields in 2-3 sentences."
            },
            {
                "role": "user",
                "content": fields_text
            }
        ],
        max_tokens=100
    )
    return response.choices[0].message["content"]