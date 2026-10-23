import os
from google.cloud import translate

def translate_live_caption(text_stream_iterator, target_language_code):
    """Translates a stream of live captions into a target language.

    Args:
        text_stream_iterator: An iterator that yields caption text strings.
        target_language_code: The language code to translate the captions into (e.g., "es" for Spanish).

    Returns:
        An iterator that yields translated caption text strings.
    """
    # Instantiates a client for Google Cloud Translation
    # This assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or other authentication methods are configured for Google Cloud.
    client = translate.TranslationServiceClient()

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    location = "global"  # Or specify a region like "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    for caption_text in text_stream_iterator:
        if not caption_text.strip():
            continue

        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [caption_text],
                "target_language_code": target_language_code,
            }
        )
        for translation in response.translations:
            yield translation.translated_text

if __name__ == "__main__":
    # This is an example of how to use the function.
    # In a real-world scenario, text_stream_iterator would come from a live caption source.

    def mock_caption_stream():
        captions = [
            "Hello, how are you today?",
            "The weather is quite nice.",
            "I hope you are having a good time.",
            "Live captioning is very useful.",
            "", # Empty caption to test skipping
            "Thank you for listening."
        ]
        for caption in captions:
            yield caption

    print("Translating live captions from English to Spanish:")
    translated_captions = translate_live_caption(mock_caption_stream(), "es")
    for translated_text in translated_captions:
        print(f"Translated: {translated_text}")

    print("\nTranslating live captions from English to French:")
    translated_captions_fr = translate_live_caption(mock_caption_stream(), "fr")
    for translated_text in translated_captions_fr:
        print(f"Translated: {translated_text}")
