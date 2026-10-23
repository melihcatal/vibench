import os
from google.cloud import translate_v2 as translate


def translate_text(text: str, target_language: str, project_id: str):
    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target_language)

    translated_text = result["translatedText"]
    detected_language = result["detectedSourceLanguage"]

    print(f"Original ({detected_language}): {text}")
    print(f"Translated ({target_language}): {translated_text}")

    return translated_text


if __name__ == "__main__":
    gcp_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not gcp_project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    customer_message = "Hello, I would like to know the status of my order."
    target_lang = "es"

    translate_text(customer_message, target_lang, gcp_project_id)
