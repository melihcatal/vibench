from openai import OpenAI

from speech_models import normalize_text


def translate_script(text: str, target_language: str = "es") -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Translate narration scripts while preserving meaning and speaker cues."},
            {"role": "user", "content": f"Translate to {target_language}: {normalize_text(text)}"},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()
