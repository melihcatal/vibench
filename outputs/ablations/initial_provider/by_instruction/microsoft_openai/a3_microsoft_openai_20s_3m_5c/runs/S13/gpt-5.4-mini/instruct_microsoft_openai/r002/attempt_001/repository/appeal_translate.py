from openai import OpenAI

from safety_client import build_client


def appeal_translate(text: str, target_language: str) -> str:
    client: OpenAI = build_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Translate this appeal into {target_language}:\n{text}",
    )
    return getattr(response, "output_text", "")
