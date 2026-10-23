from openai import OpenAI

from speech_client import client, translation_model
from speech_models import first_text


def translate_script(script: str, target_language: str) -> str:
    response = client().audio.translations.create(model=translation_model(), file=script)
    return first_text([getattr(response, "text", "")])
