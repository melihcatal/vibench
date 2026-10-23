import os
from google.cloud import translate


def translate_live_caption(
    text: str, target_language: str = "es", project_id: str = None
) -> str:
    """
    Translates a given text (live caption) into another language using Google Cloud Translation.

    Args:
        text (str): The text to translate.
        target_language (str): The language to translate the text into (e.g., "es" for Spanish).
        project_id (str): The Google Cloud project ID. If None, it will try to get it from GOOGLE_CLOUD_PROJECT env var.

    Returns:
        str: The translated text.
    """
    if project_id is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError(
            "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT env var is not set."
        )

    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language,
        }
    )

    translated_text = response.translations[0].translated_text
    print(f"Original: '{text}' -> Translated ({target_language}): '{translated_text}'")
    return translated_text


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # Make sure to set GOOGLE_CLOUD_PROJECT environment variable
    # os.environ["GOOGLE_CLOUD_PROJECT"] = "your-gcp-project-id"
    # try:
    #     translated_text = translate_live_caption("Hello, how are you today?", target_language="fr")
    #     print(f"Translated text: {translated_text}")
    # except ValueError as e:
    #     print(f"Error: {e}")
    pass
