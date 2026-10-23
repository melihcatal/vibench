from __future__ import annotations

import os

from openai import OpenAI

OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_CHAT_MODEL = "gpt-4o-mini"


def generate_spoken_brief(retrieved_results: list[dict[str, str]]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brief_prompt = "Create a concise spoken brief from these retrieved search results:\n" + "\n".join(
        f"- {item.get('title', '')}: {item.get('snippet', '')}" for item in retrieved_results
    )
    text = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[{"role": "user", "content": brief_prompt}],
    ).choices[0].message.content or ""
    audio = client.audio.speech.create(model=OPENAI_TTS_MODEL, voice="alloy", input=text)
    return text if audio else text
