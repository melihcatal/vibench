import os
from openai import OpenAI
from typing import List, Any

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_message_processing(results: List[Any]):
    content = "\n".join([str(r) for r in results])
    prompt = f"Summarize the following message processing results:\n{content}"
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content