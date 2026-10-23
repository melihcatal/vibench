from typing import Any, Dict

import openai

TRANSLATION_MODEL = "gpt-4.1-mini"


def consent_translate(text: str, target_language: str, api_key: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=api_key)
    prompt = f"Translate this identity-provider consent copy into {target_language}, preserving legal meaning and UX clarity: {text}"
    completion = client.responses.create(model=TRANSLATION_MODEL, input=prompt)
    translated = completion.output_text if hasattr(completion, "output_text") else str(completion)
    return {"target_language": target_language, "translated_text": translated, "model": TRANSLATION_MODEL}
