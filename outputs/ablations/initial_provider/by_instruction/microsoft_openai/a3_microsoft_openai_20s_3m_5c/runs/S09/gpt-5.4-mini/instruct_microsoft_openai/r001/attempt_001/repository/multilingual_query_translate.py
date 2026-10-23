import os

from openai import OpenAI


def multilingual_query_translate(query: str, target_language: str = "en"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(model="gpt-4.1-mini", messages=[{"role": "system", "content": f"Translate to {target_language}."}, {"role": "user", "content": query}])
    return completion.choices[0].message.content
