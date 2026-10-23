from __future__ import annotations

from safety_client import DEFAULT_CHAT_MODEL, get_openai_client


def moderation_summary(decisions: list[dict]) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=DEFAULT_CHAT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize moderation outcomes for an internal trust and safety queue in concise prose.",
            },
            {
                "role": "user",
                "content": f"Create a short moderation summary for these decisions: {decisions}",
            },
        ],
    )
    return response.output_text
