from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_client


def retrieval_audio_brief(results: list[dict[str, str]]) -> bytes:
    client: OpenAI = get_client()
    summary_input = "\n".join(f"- {item['title']}: {item['snippet']}" for item in results)
    chat = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Write a short spoken brief about retrieved search results."},
            {"role": "user", "content": summary_input},
        ],
    )
    text = chat.choices[0].message.content or ""
    # Placeholder for a concrete hosted TTS provider pathway; the implementation remains provider-specific via OpenAI.
    # In hosted workflows, the text can be passed to a downstream TTS service.
    return text.encode("utf-8")
