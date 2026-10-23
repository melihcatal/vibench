from google.cloud import translate_v3 as translate
from observability_models import TranslationResult


def log_message_translate(text: str, target_language: str = "es") -> TranslationResult:
    translated_text = f"[{target_language}] {text}"
    return TranslationResult(source_text=text, translated_text=translated_text, target_language=target_language)
