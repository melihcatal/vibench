from google.cloud import translate_v2 as translate

def translate_appeal(text, target_language):
    """Translates text into the target language using Google Cloud Translation."""
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == "__main__":
    # Example usage (replace with actual appeal text and target language)
    appeal_text = "This is an appeal regarding the decision made on my application."
    target_language = "es"  # Translate to Spanish
    translated_text = translate_appeal(appeal_text, target_language)
    print(f"Original text: {appeal_text}")
    print(f"Translated text ({target_language}): {translated_text}")
