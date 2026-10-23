from typing import Dict, Any

from openai import OpenAI


def image_summary(results: Dict[str, Any]) -> str:
    client = OpenAI()
    payload = str(results)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize visual analysis results briefly."},
            {"role": "user", "content": payload},
        ],
    )
    return response.choices[0].message.content or ""
