import os
from openai import OpenAI
from speech_models import TranscriptEvent

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_transcript_chunk(events: list[TranscriptEvent]) -> str:
    transcript = " ".join([event.text for event in events if event.is_final])
    if not transcript:
        return ""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # OpenAI's concrete model identifier
        messages=[
            {"role": "system", "content": "Summarize the following meeting transcript:"},
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content.strip()