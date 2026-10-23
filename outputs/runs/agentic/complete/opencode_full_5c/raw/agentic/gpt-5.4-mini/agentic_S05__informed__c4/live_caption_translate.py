from typing import Iterable, List

from deepl import Translator

from speech_models import TranscriptEvent, normalize_text


def translate_live_captions(
    events: Iterable[TranscriptEvent], target_language: str
) -> List[str]:
    translator = Translator(auth_key="", server_url="https://api-free.deepl.com")
    translated = []
    for event in events:
        text = normalize_text(event.text)
        if text:
            translated.append(
                translator.translate_text(text, target_lang=target_language).text
            )
    return translated
