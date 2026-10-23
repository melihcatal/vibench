from typing import Iterable

from openai import OpenAI

from speech_models import TranscriptEvent, normalize_text


def summarize_meeting(events: Iterable[TranscriptEvent]) -> str:
    client = OpenAI()
    transcript = "\n".join(
        normalize_text(event.text) for event in events if normalize_text(event.text)
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the meeting transcript."},
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content or ""
