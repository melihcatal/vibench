from google.cloud import translate_v2 as translate
import os

def translate_alt_text(text: str, target_language: str = "es") -> str:
    """Translates alt text to a target language using Google Cloud Translation."""
    client = translate.Client()

    # The Google Cloud project ID can be inferred from the environment
    # or explicitly set via client = translate.Client(project=project_id)
    # We assume GOOGLE_APPLICATION_CREDENTIALS is set.

    result = client.translate(text, target_language=target_language)
    return result['translatedText']

if __name__ == '__main__':
    # Example usage
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    # english_text = "A fluffy cat sitting on a couch."
    # spanish_text = translate_alt_text(english_text, "es")
    # print(f"Original: {english_text}")
    # print(f"Translated (Spanish): {spanish_text}")
    pass