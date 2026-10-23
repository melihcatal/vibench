import os
from google.cloud import translate_v2 as translate

def translate_script(text: str, target_language: str = "es", source_language: Optional[str] = None) -> dict:
    """Translates narration scripts using Google Cloud Translation."""
    client = translate.Client()

    # Target language can be specified as a BCP-47 language code (e.g., 'es' for Spanish)
    # or a language name (e.g., 'Spanish').
    # The client automatically detects the source language if not provided.
    translation_result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language
    )

    # The result contains the translated text, detected source language, and the original text.
    return {
        "original_text": text,
        "translated_text": translation_result["translatedText"],
        "source_language": translation_result["detectedSourceLanguage"],
        "target_language": target_language
    }

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    script_to_translate = "The quick brown fox jumps over the lazy dog."
    translated_content = translate_script(script_to_translate, target_language="fr")
    print(f"Original: {translated_content["original_text"]}")
    print(f"Translated (fr): {translated_content["translated_text"]}")
    print(f"Detected Source Language: {translated_content["source_language"]}")

    script_to_translate_zh = "你好世界"
    translated_content_en = translate_script(script_to_translate_zh, target_language="en")
    print(f"Original: {translated_content_zh}")
    print(f"Translated (en): {translated_content_en["translated_text"]}")
    print(f"Detected Source Language: {translated_content_en["source_language"]}")
