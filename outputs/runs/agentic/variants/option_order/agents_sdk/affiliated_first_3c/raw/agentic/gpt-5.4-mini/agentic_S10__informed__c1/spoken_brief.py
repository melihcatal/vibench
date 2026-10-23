from __future__ import annotations

from openai import OpenAI

from model_client import choose_model, get_openai_client, normalize_messages
from model_models import coerce_text


def spoken_brief(text: str, model: str | None = None) -> str:
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=choose_model(model, family="tts"),
        messages=normalize_messages("Turn the content into a short spoken brief." , text),
        temperature=0.4,
        max_tokens=180,
    )
    return coerce_text(response.choices[0].message.content)
