from google.cloud import translate_v2 as translate
import os

def translate_caption(text: str, target_language: str = "es") -> str:
    translate_client = translate.Client()

    # Target language can be a language code or a language name
    # e.g., "fr" for French, "es" for Spanish
    # Google Cloud Translation automatically detects the source language.
    result = translate_client.translate(text, target_language=target_language)

    # print(f"Text: {result['input']}")
    # print(f"Translation: {result['translatedText']}")
    # print(f"Detected source language: {result['detectedSourceLanguage']}")

    return result['translatedText']

if __name__ == "__main__":
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set as an environment variable
    # or authenticated via `gcloud auth application-default login`
    
    example_caption = "Hello, how are you doing today?"
    translated_text = translate_caption(example_caption, target_language="fr")
    print(f"Original: {example_caption}")
    print(f"Translated (French): {translated_text}")

    example_caption_2 = "This is a test sentence for translation."
    translated_text_2 = translate_caption(example_caption_2, target_language="de")
    print(f"Original: {example_caption_2}")
    print(f"Translated (German): {translated_text_2}")
