import os
from openai import OpenAI
from typing import List, Dict, Any

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_message_processing(results: List[Dict[str, Any]]) -> str:
    summary_prompt = "Provide a concise summary of the following message processing results:\\n\\n"
    for i, result in enumerate(results, 1):
        summary_prompt += f"{i}. {result}\\n"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content