from vision_client import translate_text


def alt_text_translate(text: str, target_language: str) -> str:
    return translate_text(text, target_language)
