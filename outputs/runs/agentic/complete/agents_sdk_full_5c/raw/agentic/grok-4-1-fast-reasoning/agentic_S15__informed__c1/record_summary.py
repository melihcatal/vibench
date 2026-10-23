import os
import json
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def record_summary(records: List[Dict[str, Any]]) -> str:
    prompt = "Provide a concise summary of the following document records:\\n\\n" + json.dumps(records, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content