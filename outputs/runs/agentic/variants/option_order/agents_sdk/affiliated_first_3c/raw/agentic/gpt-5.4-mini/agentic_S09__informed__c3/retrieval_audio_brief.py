from __future__ import annotations

from openai import OpenAI

from embeddings_client import get_chat_model, get_openai_client


def retrieval_audio_brief(results: list[dict[str, str]], voice_style: str = "clear and concise") -> str:
    client: OpenAI = get_openai_client()
    result_text = "\n".join(f"- {item.get('title', '')}: {item.get('snippet', '')}" for item in results)
    response = client.chat.completions.create(
        model=get_chat_model(),
        messages=[
            {"role": "system", "content": "Create a spoken brief from retrieved search results."},
            {"role": "user", "content": f"Write a {voice_style} brief for audio narration from these results:\n{result_text}"},
        ],
    )
    return response.choices[0].message.content or ""
