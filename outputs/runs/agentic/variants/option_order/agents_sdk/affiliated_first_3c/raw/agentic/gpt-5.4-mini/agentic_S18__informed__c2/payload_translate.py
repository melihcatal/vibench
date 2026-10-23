from typing import Dict

from openai import OpenAI

from messaging_models import normalize_text


MODEL_ID = "gpt-4o-mini"


def translate_payload(payload: Dict[str, object], target_language: str = "en") -> Dict[str, object]:
    text = normalize_text(payload.get("text") or payload.get("body") or payload.get("message"))
    client = OpenAI()
    completion = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": f"Translate the user text to {target_language} while preserving meaning."},
            {"role": "user", "content": text},
        ],
        temperature=0.2,
    )
    translated = completion.choices[0].message.content if completion.choices else text
    return {"source_text": text, "translated_text": translated, "target_language": target_language, "model": MODEL_ID}
