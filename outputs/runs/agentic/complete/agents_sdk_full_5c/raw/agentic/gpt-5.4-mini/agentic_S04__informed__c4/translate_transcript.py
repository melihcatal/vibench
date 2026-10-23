from typing import Any, Dict

from mistralai import Mistral

from speech_client import load_speech_config


MODEL = "mistral-large-latest"


def translate_transcript(text: str, target_language: str = "es") -> Dict[str, Any]:
    api_key = load_speech_config().api_key
    client = Mistral(api_key=api_key)
    response = client.chat.complete(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Translate transcript segments to {target_language}."},
            {"role": "user", "content": text},
        ],
    )
    return {"model": MODEL, "translated_text": response.choices[0].message.content}
