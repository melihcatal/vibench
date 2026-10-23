import os
import deepl
from messaging_models import Event

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


def translate_payload(event: Event, target_lang: str = "ES") -> Event:
    text = str(event.payload)
    translation = translator.translate_text(text, target_lang=target_lang)
    event.payload["translated"] = translation.text
    return event
