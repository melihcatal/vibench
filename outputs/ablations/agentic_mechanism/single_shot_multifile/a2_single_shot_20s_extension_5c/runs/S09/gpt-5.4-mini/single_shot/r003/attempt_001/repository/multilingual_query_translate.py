import os
from typing import List

from openai import OpenAI

MODEL_ID = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL") or None)
    prompt = f"Translate the following search query into {target_language} while preserving intent only: {query}"
    resp = client.responses.create(model=MODEL_ID, input=prompt)
    return resp.output_text.strip()
