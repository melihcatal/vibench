from __future__ import annotations

from openai import OpenAI


SUMMARY_MODEL = "gpt-4.1-mini"


def moderation_summary(decisions: list[dict]) -> dict[str, str]:
    client = OpenAI()
    prompt = {
        "role": "user",
        "content": (
            "Summarize these moderation decisions for an internal trust and safety queue. "
            "Include counts, repeated risk themes, and recommended next action in under 120 words.\n"
            f"Decisions: {decisions}"
        ),
    }
    response = client.responses.create(model=SUMMARY_MODEL, input=[prompt])
    return {
        "provider": "openai",
        "model": SUMMARY_MODEL,
        "summary": response.output_text,
    }
