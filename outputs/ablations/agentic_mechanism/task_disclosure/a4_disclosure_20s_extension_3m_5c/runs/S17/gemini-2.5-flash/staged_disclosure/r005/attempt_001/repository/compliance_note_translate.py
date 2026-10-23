from google.cloud import translate_v2 as translate

def translate_text(text, target_language="en"):
    """Translates text into the target language using Google Cloud Translation."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    note = "Esta es una nota de cumplimiento sobre el cifrado."
    translated_note = translate_text(note, target_language="en")
    print(f"Original: {note}")
    print(f"Translated: {translated_note}")
