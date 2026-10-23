from __future__ import annotations

from openai import OpenAI

from speech_models import SpeechResult


TRANSLATION_MODEL = "gpt-4o-mini"


def translate_transcript(result: SpeechResult, target_language: str = "es") -> str:
    client = OpenAI()
    transcript_text = result.text or "\n".join(segment.text for segment in result.segments)
    response = client.chat.completions.create(
        model=TRANSLATION_MODEL,
        messages=[
            {"role": "system", "content": "Translate transcript segments faithfully and preserve speaker/timestamp cues when present."},
            {"role": "user", "content": f"Translate to {target_language}:\n{transcript_text}"},
        ],
        temperature=0.1,
    )
    return response.choices[0].message.content or ""
