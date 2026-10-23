from __future__ import annotations

import os

from openai import OpenAI

from embeddings_client import get_chat_model, get_openai_client


def corpus_safety(text: str) -> dict[str, object]:
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {"role": "system", "content": "Assess whether text is safe to process for embedding and search."},
            {"role": "user", "content": f"Evaluate this corpus text for safety issues and provide a short label: {text}"},
        ],
    )
    content = response.choices[0].message.content or ""
    return {"provider": "openai", "safe": "unsafe" not in content.lower(), "analysis": content}
