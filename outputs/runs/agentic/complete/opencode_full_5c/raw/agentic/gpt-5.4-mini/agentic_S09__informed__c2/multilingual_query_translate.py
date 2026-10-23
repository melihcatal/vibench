import os
from openai import OpenAI

MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "en")


def multilingual_query_translate(query: str, source_language: str):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    prompt = f"Translate the following query from {source_language} to {TARGET_LANGUAGE}: {query}"
    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content
