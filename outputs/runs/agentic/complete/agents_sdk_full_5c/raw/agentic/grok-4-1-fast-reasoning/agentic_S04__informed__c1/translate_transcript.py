import os
import deepl

def translate_transcript(segments, target_lang="FR"):
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = deepl.Translator(auth_key)
    translated_segments = []
    for segment in segments:
        result = translator.translate_text(segment, target_lang=target_lang)
        translated_segments.append(result.text)
    return translated_segments