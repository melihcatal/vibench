from google.cloud import translate_v2 as translate
import os


def appeal_translate(text, target_language="en"):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
    # or authentication configured otherwise.
    # For local development, you might set GOOGLE_APPLICATION_CREDENTIALS to a path to your service account key file.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    return result["translatedText"]


if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS environment variable to be set)
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account key file."
        )
    else:
        appeal_text_french = "Ceci est un appel pour ma modération de contenu."
        translated_text = appeal_translate(appeal_text_french, target_language="en")
        print(f"Original (French): '{appeal_text_french}'")
        print(f"Translated (English): '{translated_text}'")

        appeal_text_spanish = "Quiero apelar esta decisión."
        translated_text_2 = appeal_translate(appeal_text_spanish, target_language="en")
        print(f"Original (Spanish): '{appeal_text_spanish}'")
        print(f"Translated (English): '{translated_text_2}'")
