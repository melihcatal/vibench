from translation_client import get_translation_client


def quality_summary(text: str, source_language_code: str, target_language_code: str):
    client = get_translation_client()
    translated = client.translate_text(text, source_language_code, target_language_code)
    return {
        "provider": "aws.translate",
        "source_language_code": source_language_code,
        "target_language_code": target_language_code,
        "issues": [] if translated else ["empty_translation"],
    }
