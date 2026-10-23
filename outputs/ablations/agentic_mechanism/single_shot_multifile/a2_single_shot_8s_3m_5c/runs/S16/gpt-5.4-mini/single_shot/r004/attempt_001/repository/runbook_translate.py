from dataclasses import dataclass

from google.cloud import translate_v3

DEFAULT_TARGET_LANGUAGE = "es"


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str


def translate_runbook_notes(text: str, target_language: str = DEFAULT_TARGET_LANGUAGE, project_id: str = "") -> TranslationResult:
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global" if project_id else "locations/global"
    response = client.translate_text(contents=[text], target_language_code=target_language, parent=parent, mime_type="text/plain")
    translated = response.translations[0].translated_text if response.translations else ""
    return TranslationResult(source_text=text, translated_text=translated, target_language=target_language)