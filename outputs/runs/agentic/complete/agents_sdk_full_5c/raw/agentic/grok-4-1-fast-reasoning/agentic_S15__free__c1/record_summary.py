import os
import json
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def record_summary(records: List[Dict[str, Any]]) -> str:
    text = json.dumps(records, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Please provide a concise summary of these document records:\n\n{text}"}]
    )
    return response.choices[0].message.content
