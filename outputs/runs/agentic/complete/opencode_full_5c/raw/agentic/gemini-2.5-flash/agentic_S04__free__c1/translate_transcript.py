import os
from google.cloud import translate_v3 as translate


def translate_text(project_id: str, target_language_code: str, texts: list[str]):
    """Translates a list of texts using Google Cloud Translation.

    Args:
        project_id: The Google Cloud project ID.
        target_language_code: The language code to translate to (e.g., "es").
        texts: A list of text strings to translate.

    Returns:
        A list of translated text strings.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language_code,
        }
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)
    return translated_texts


if __name__ == "__main__":
    # Example usage
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    target_language_code = "es"
    transcript_segments = [
        "Hello, how are you today?",
        "I am doing well, thank you for asking.",
        "What are your plans for the weekend?",
    ]

    if project_id:
        print(
            f"Translating {len(transcript_segments)} segments to {target_language_code}..."
        )
        translated_segments = translate_text(
            project_id, target_language_code, transcript_segments
        )
        for original, translated in zip(transcript_segments, translated_segments):
            print(f"Original: {original}")
            print(f"Translated: {translated}")
            print("-" * 20)
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
