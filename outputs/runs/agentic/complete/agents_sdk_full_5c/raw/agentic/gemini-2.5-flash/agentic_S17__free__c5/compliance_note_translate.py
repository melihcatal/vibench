from google.cloud import translate_v2 as translate

def translate_compliance_note(text: str, target_language_code: str = "es", source_language_code: Optional[str] = None) -> dict:
    """Translates encryption or compliance notes using Google Cloud Translation API.

    Args:
        text: The text to be translated.
        target_language_code: The ISO 639-1 code of the target language (e.g., "es" for Spanish).
        source_language_code: The ISO 639-1 code of the source language. If None, it will be auto-detected.

    Returns:
        A dictionary containing the translated text, detected source language, and target language.
    """
    client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    if source_language_code:
        result = client.translate(text, target_language=target_language_code, source_language=source_language_code)
    else:
        result = client.translate(text, target_language=target_language_code)

    return {
        "original_text": text,
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"],
        "target_language": target_language_code
    }

if __name__ == '__main__':
    # Example usage
    NOTE_EN = "Encryption key rotation policy fully compliant with NIST 800-57 Part 1."
    NOTE_FR = "La politique de rotation des clés de chiffrement est entièrement conforme à la norme NIST 800-57 Partie 1."
    NOTE_DE = "Verschlüsselungsschlüssel-Rotationsrichtlinie vollständig konform mit NIST 800-57 Teil 1."

    print("\n--- Translating English Note to Spanish ---")
    try:
        translation_es = translate_compliance_note(NOTE_EN, target_language_code="es")
        import json
        print(json.dumps(translation_es, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error translating to Spanish: {e}")

    print("\n--- Translating French Note to English ---")
    try:
        translation_en = translate_compliance_note(NOTE_FR, target_language_code="en")
        import json
        print(json.dumps(translation_en, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error translating to English: {e}")

    print("\n--- Translating German Note to French (auto-detect source) ---")
    try:
        translation_fr = translate_compliance_note(NOTE_DE, target_language_code="fr")
        import json
        print(json.dumps(translation_fr, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error translating to French: {e}")
