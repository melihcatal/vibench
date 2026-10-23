import os
from openai import OpenAI

def multilingual_query_translate(query: str, target_language: str = "English") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY required")
    client = OpenAI(api_key=api_key)
    prompt = f"Translate the following query to {target_language}:\\n\\n{query}\\n\\nProvide only the translated query."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert translator. Output ONLY the translation, nothing else."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()