# [LATER-STEP] unsafe_copy_check.py

# Checks localized copy for unsafe content using OpenAI Moderation API (hosted service).
import os
import json
from openai import OpenAI

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("Set OPENAI_API_KEY environment variable")

client = OpenAI(api_key=openai_api_key)


def check_unsafe(localized_texts: list[str]) -> list[bool]:
    """Return a list of booleans indicating unsafe (True) or safe (False) content.","""
    messages = [
        {
            "role": "system",
            "content": "You are a content safety evaluator. For each input text, return ONLY True if the text contains unsafe content (hate speech, self-harm, sexual content, etc.), otherwise return False.",
        }
    ]
    for txt in localized_texts:
        messages.append({"role": "user", "content": txt})
    responses = client.moderations.create(
        input=messages,
        model="openai/moderations",  # using moderation endpoint
    )
    # The API returns a list of moderation results in the 'results' field
    results = [r["flagged"] for r in responses["results"]]
    return results
