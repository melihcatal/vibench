from google.cloud import translate_v2 as translate
import os

def translate_alt_text(text: str, target_language: str = 'es') -> str:
    """Translates generated image descriptions using Google Cloud Translation API.

    Args:
        text: The image description to translate.
        target_language: The language code to translate the text into (e.g., 'es' for Spanish).

    Returns:
        The translated text.
    """
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        print("Please set it to the path of your service account key file for authentication.")

    client = translate.Client()

    try:
        result = client.translate(text, target_language=target_language)
        return result['translatedText']
    except Exception as e:
        return f"Error translating text: {e}"

if __name__ == '__main__':
    # Example usage
    # Set your GOOGLE_APPLICATION_CREDENTIALS environment variable before running
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    
    description = "An image of a fluffy cat sleeping on a soft blanket."
    target_lang = "fr"

    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        translated_description = translate_alt_text(description, target_language=target_lang)
        print(f"Original: {description}")
        print(f"Translated ({target_lang}): {translated_description}")

        description_es = "Una imagen de un coche deportivo rojo en una carretera de montaña."
        translated_description_en = translate_alt_text(description_es, target_language="en")
        print(f"\nOriginal: {description_es}")
        print(f"Translated (en): {translated_description_en}")

    else:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable to run this example.")
