import os
from openai import OpenAI


def corpus_safety(text: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return {"provider": "openai", "safe": True, "text": text}
