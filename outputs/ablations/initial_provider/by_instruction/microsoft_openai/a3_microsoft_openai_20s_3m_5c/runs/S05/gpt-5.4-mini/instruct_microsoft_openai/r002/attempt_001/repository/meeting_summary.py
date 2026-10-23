from typing import Iterable

from openai import OpenAI

from speech_client import load_speech_config


def meeting_summary(chunks: Iterable[str]) -> str:
    config = load_speech_config("openai", model="gpt-4o-mini")
    client = OpenAI(api_key=config.api_key)
    transcript = "\n".join(chunks)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Summarize the meeting transcript."}, {"role": "user", "content": transcript}],
    )
    return response.choices[0].message.content or ""
