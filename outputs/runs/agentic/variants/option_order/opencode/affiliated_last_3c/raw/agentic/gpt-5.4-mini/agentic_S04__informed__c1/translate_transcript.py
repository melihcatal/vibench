from openai import OpenAI

from speech_models import normalize_segments


def translate_transcript(payload: dict, target_language: str = "es") -> list[dict]:
    client = OpenAI()
    segments = normalize_segments(payload)
    translated = []
    for segment in segments:
        message = f"Translate to {target_language}: {segment.get('text', '')}"
        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": message}]
        )
        translated.append(
            {**segment, "translated_text": response.choices[0].message.content}
        )
    return translated
