from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """Translates text into the target language using Google Cloud Translation."""
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

if __name__ == "__main__":
    text_to_translate = "El texto de la apelación debe ser revisado."
    translated_text = translate_text(text_to_translate, "en")
    print(f"Original: {text_to_translate}")
    print(f"Translated: {translated_text}")
