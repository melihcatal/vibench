import os
from typing import List
from openai import OpenAI
from database_models import Document

def generate_record_summary(records: List[Document]) -> str:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    contents = '\n'.join([str(record) for record in records])
    prompt = f"Summarize the following document records concisely:\n\n{contents}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content