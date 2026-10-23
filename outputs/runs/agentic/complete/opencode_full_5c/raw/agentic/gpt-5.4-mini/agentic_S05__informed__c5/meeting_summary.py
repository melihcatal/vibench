import os

from openai import OpenAI

from speech_models import TranscriptEvent, normalize_transcript


def meeting_summary(events: list[TranscriptEvent]) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    transcript = "\n".join(normalize_transcript(event.text) for event in events)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize the meeting clearly and concisely.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content or ""
