import openai
import os
import json
from typing import List, Dict, Any


def summarize_key_usage(events: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the key usage and crypto events listed below in a concise report, highlighting any anomalies or high usage:\\n\\n"
        + json.dumps(events, indent=2)
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a crypto audit assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
