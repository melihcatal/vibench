import os
from typing import List, Dict, Any
from openai import OpenAI


def record_summary(records: List[Dict[str, Any]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "OPENAI_API_KEY not set."
    client = OpenAI(api_key=api_key)
    if not records:
        return "No records to summarize."
    contents = "\\n".join([str(record) for record in records])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Provide a concise summary of these document records:\\n\\n{contents[:4000]}",
            }
        ],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content
