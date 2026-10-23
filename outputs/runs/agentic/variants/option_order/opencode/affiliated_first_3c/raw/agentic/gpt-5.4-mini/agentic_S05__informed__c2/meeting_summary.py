from typing import Iterable

from openai import OpenAI

from speech_models import TranscriptEvent, normalize_transcript_text


def summarize_meeting(chunks: Iterable[TranscriptEvent]) -> str:
    client = OpenAI()
    transcript = "\n".join(
        normalize_transcript_text(chunk.text)
        for chunk in chunks
        if normalize_transcript_text(chunk.text)
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the meeting transcript."},
            {"role": "user", "content": transcript},
        ],
    )
    return completion.choices[0].message.content or ""
