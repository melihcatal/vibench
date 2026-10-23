from openai import OpenAI

from speech_models import normalize_transcript_text


def translate_transcript(
    segments: list[dict[str, str]], target_language: str = "es"
) -> str:
    client = OpenAI()
    text = normalize_transcript_text([segment.get("text", "") for segment in segments])
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": f"Translate to {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content or ""
