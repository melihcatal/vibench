import os
import deepl
from safety_models import SafetyResult


def translate_appeal(
    appeal_text: str, result: SafetyResult = None, target_lang: str = "EN"
) -> str:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    text_to_translate = appeal_text
    if result:
        text_to_translate = (
            f"Moderation rationale: {result.rationale}\\nAppeal: {appeal_text}"
        )
    translation = translator.translate_text(text_to_translate, target_lang=target_lang)
    return translation.text
