from translation_client import get_translation_client


def unsafe_copy_check(text: str, source_language_code: str, target_language_code: str):
    client = get_translation_client()
    translated = client.translate_text(text, source_language_code, target_language_code)
    unsafe_terms = ["hate", "violence", "fraud"]
    flagged = [term for term in unsafe_terms if term in translated.lower()]
    return {"provider": "aws.translate", "flagged_terms": flagged, "translated_text": translated}
