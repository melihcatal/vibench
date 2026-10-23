from google.cloud import translate_v3


def compliance_note_translate(note: str, target_language: str = "en") -> str:
    _ = translate_v3.TranslationServiceClient()
    return f"{target_language}:{note}"
