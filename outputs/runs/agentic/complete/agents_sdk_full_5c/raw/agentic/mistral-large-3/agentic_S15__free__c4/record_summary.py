from typing import Dict, Any
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
OPENAI_MODEL = "gpt-4o-mini"

client = OpenAI(api_key=OPENAI_API_KEY)

def summarize_record(document: Dict[str, Any]) -> str:
    """
    Summarizes a document record using OpenAI's GPT-4o-mini model.
    """
    prompt = f"Summarize the following document in 2-3 sentences:\n\n{document}"
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()