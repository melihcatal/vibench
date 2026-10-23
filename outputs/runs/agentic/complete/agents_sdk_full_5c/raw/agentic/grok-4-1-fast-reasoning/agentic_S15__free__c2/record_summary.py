import os
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_records(documents: List[Dict[str, Any]]) -> str:
    texts = '\n\n'.join([str(doc) for doc in documents])
    prompt = f"Please provide a concise summary of the following document records:\\n\\n{texts}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content