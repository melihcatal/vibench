from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    notes = "Estas son algunas notas de cumplimiento sobre el cifrado."
    translated_notes = translate_text(notes, "en")
    print(f"Original: {notes}")
    print(f"Translated: {translated_notes}")
