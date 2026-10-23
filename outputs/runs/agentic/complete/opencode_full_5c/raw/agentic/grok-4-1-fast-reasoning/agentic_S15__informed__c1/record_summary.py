import os
from openai import OpenAI
from typing import List, Dict, Any


def summarize_records(records: List[Dict[str, Any]]) -> str:
    texts = "\\n".join([str(record) for record in records])
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of these document records:\\n\\n{texts}",
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content
