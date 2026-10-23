from __future__ import annotations

from openai import OpenAI

from messaging_models import extract_text


def summarize_message_result(payload: dict, processing_status: str) -> dict[str, str]:
    client = OpenAI()
    text = extract_text(payload)
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Summarize message processing outcomes in one concise sentence.",
            },
            {
                "role": "user",
                "content": f"Status: {processing_status}\nPayload: {text}",
            },
        ],
    )
    return {"summary": response.output_text.strip(), "model": "gpt-4.1-mini"}
