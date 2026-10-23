from typing import List

from openai import OpenAI


def moderation_summary(decisions: List[dict]) -> str:
    client = OpenAI()
    prompt = f"Summarize these moderation decisions for an internal reviewer: {decisions}"
    resp = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return resp.output_text
