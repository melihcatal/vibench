import os
from openai import OpenAI

def multilingual_query_translate(query: str, source_lang: str = "auto", target_lang: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"Translate the following query from {source_lang} to {target_lang}:\n\n{query}\n\nProvide only the translated text."
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()