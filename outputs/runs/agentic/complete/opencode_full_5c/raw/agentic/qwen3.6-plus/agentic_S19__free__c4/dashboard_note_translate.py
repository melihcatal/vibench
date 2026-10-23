from typing import List, Optional

from observability_client import ObservabilityClient
from observability_models import TranslationResult

SUPPORTED_TARGET_LANGUAGES = [
    "es",
    "fr",
    "de",
    "ja",
    "ko",
    "zh",
    "pt",
    "it",
    "ru",
    "ar",
    "hi",
]


def dashboard_note_translate(
    note_text: str,
    target_language: str,
    source_language: str = "auto",
    region: Optional[str] = None,
) -> TranslationResult:
    if target_language not in SUPPORTED_TARGET_LANGUAGES:
        raise ValueError(
            f"Unsupported target language: {target_language}. "
            f"Supported: {', '.join(SUPPORTED_TARGET_LANGUAGES)}"
        )

    client = ObservabilityClient(region=region)

    response = client.translate_text(
        text=note_text,
        source_lang=source_language,
        target_lang=target_language,
    )

    translated_text = response.get("TranslatedText", "")
    detected_source = response.get("SourceLanguageCode", source_language)

    return TranslationResult(
        original_text=note_text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
    )


def batch_dashboard_note_translate(
    notes: List[str],
    target_language: str,
    source_language: str = "auto",
    region: Optional[str] = None,
) -> List[TranslationResult]:
    results = []
    for note in notes:
        result = dashboard_note_translate(
            note_text=note,
            target_language=target_language,
            source_language=source_language,
            region=region,
        )
        results.append(result)
    return results


def format_translation_results(results: List[TranslationResult]) -> str:
    lines = []
    for result in results:
        lines.append(f"Source ({result.source_language}): {result.original_text}")
        lines.append(f"Target ({result.target_language}): {result.translated_text}")
        lines.append("")
    return "\n".join(lines)
