import os
from typing import List, Dict, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_message_processing(results: List[Dict[str, Any]]) -> str:
    context = json.dumps(results, indent=2)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Summarize these message processing results:\n{context}"}
        ]
    )
    return response.choices[0].message.content
