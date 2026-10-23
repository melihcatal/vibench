
from google.cloud import translate_v2 as translate
import os

def translate_text(text, target_language, project_id=None):
    """Translates text into the target language.

    Args:
        text: The text to translate.
        target_language: The language to translate the text to (e.g., "es" for Spanish).
        project_id: The ID of the Google Cloud project. If not provided,
                    it will attempt to use the GOOGLE_CLOUD_PROJECT environment variable.

    Returns:
        The translated text.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.Client(project=project_id)

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = client.translate(text, target_language=target_language)

    return result["translatedText"]

if __name__ == "__main__":
    # Example usage:
    # Set your Google Cloud Project ID as an environment variable or pass it directly.
    # export GOOGLE_CLOUD_PROJECT="your-project-id"
    # or
    # translated_text = translate_text("Hello, world!", "es", project_id="your-project-id")

    # This example assumes GOOGLE_CLOUD_PROJECT environment variable is set.
    # Replace with your actual project ID or set the environment variable.
    try:
        translated_text = translate_text("Hello, world!", "es")
        print(f"Original text: Hello, world!")
        print(f"Translated text (Spanish): {translated_text}")

        translated_text_french = translate_text("How are you?", "fr")
        print(f"Original text: How are you?")
        print(f"Translated text (French): {translated_text_french}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or provide the project_id argument.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
