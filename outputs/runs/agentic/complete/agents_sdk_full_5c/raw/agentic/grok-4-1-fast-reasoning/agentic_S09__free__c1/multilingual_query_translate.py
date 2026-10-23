import os
from typing import Optional
from openai import OpenAI

def multilingual_query_translate(query: str, target_lang: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"Translate the following query to {target_lang}: '{query}'\\nProvide only the translated text, nothing else."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
