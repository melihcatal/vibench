import os
import json
from openai import OpenAI
from typing import List
from database_models import Document


def summarize_records(records: List[Document]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize these document records concisely:\\n" + json.dumps(
        records, indent=2
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content
