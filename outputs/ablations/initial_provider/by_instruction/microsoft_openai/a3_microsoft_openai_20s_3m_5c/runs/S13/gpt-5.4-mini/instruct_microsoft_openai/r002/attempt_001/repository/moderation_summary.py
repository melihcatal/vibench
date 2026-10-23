from openai import OpenAI

from safety_client import build_client


def moderation_summary(text: str) -> str:
    client: OpenAI = build_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Summarize the moderation decision history for this text:\n{text}",
    )
    return getattr(response, "output_text", "")
