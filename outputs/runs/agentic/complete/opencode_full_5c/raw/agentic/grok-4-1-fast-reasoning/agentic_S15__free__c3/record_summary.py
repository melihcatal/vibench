import openai
import os
from typing import List, Dict, Any

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_records(records: List[Dict[str, Any]]) -> str:
    texts = "\n".join(str(record) for record in records)
    prompt = f"Summarize the following records:\n{texts}"
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
