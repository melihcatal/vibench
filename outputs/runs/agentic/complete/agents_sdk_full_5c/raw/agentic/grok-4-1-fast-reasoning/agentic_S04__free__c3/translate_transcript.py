import os
import deepl

def translate_transcript(segments: list[str], target_lang: str = "EN-US") -> list[str]:
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required.")
    translator = deepl.Translator(api_key)
    translated_segments = []
    for segment in segments:
        result = translator.translate_text(segment, target_lang=target_lang)
        translated_segments.append(result.text)
    return translated_segments