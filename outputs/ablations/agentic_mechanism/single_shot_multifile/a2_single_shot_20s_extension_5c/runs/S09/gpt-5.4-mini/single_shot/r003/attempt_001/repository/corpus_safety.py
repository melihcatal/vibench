import os
from typing import List

from openai import OpenAI

MODEL_ID = os.getenv("OPENAI_CHAT_MODEL", "gpt-4.1-mini")


def corpus_safety(texts: List[str]) -> bool:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL") or None)
    prompt = "Assess whether the following corpus texts are safe to embed for semantic retrieval. Reply only SAFE or UNSAFE.\n\n" + "\n".join(texts[:50])
    resp = client.responses.create(model=MODEL_ID, input=prompt)
    return "SAFE" in resp.output_text.upper()
