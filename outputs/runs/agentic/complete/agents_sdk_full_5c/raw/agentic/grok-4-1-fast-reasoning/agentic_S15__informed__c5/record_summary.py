import os
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_records(records: List[Dict[str, Any]]) -> str:
    records_text = "\n".join([str(record) for record in records])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Please provide a concise summary of the following document records:\\n\\n{records_text}"
            }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content
