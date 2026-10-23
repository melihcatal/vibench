import os
from openai import OpenAI
from typing import List, Dict, Any

def summarize_messages(messages: List[Dict[str, Any]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize the processing results from these messages:\\n" + "\\n".join([str(m) for m in messages])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content