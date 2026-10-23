import os
import json
from openai import OpenAI
from typing import List, Dict, Any


def summarize_records(records: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = json.dumps(records, indent=2)
    prompt = f"Provide a concise summary of the following document records:\\n\\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )
    return response.choices[0].message.content
