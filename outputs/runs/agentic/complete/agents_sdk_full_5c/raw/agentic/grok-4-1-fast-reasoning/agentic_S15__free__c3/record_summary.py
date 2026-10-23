import openai
import os
from typing import List, Dict, Any

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def summarize_records(records: List[Dict[str, Any]]) -> str:
    record_texts = '\n\n'.join([str(record.get('data', '')) for record in records])
    prompt = f"Please provide a concise summary of the following document records:\n\n{record_texts}"
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content
