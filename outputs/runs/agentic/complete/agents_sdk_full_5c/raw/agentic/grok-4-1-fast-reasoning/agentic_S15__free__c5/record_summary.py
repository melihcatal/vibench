import os
from openai import OpenAI
from typing import List, Dict, Any

def summarize_records(records: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    texts = "\n".join([str(record) for record in records])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Please provide a concise summary of the following records:\n{texts}"}]
    )
    return response.choices[0].message.content