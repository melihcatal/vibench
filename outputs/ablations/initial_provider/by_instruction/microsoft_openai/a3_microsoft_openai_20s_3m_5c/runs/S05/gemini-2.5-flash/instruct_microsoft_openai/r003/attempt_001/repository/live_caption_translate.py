import os
from google.cloud import translate_v2 as translate

# This file translates live captions into another language using Google Cloud Translation API.

def live_caption_translator(target_language: str = "es", project_id: str = None):
    client = translate.Client(project=project_id)

    # In a real scenario, captions would be streamed into this function.
    # For demonstration, we'll use a generator to simulate receiving captions.
    def caption_stream_source():
        captions = [
            "Hello, how are you?",
            "This is a live transcript example.",
            "We are testing the translation service."
        ]
        for caption in captions:
            yield caption

    print(f"Starting live caption translation to {target_language} using Google Cloud Translation...")
    for caption_chunk in caption_stream_source():
        print(f"Original: {caption_chunk}")
        try:
            # The `translate` method can infer the source language if not provided.
            result = client.translate(caption_chunk, target_language=target_language)
            translated_text = result["translatedText"]
            yield f"Translated: {translated_text}"
        except Exception as e:
            yield f"Translation Error: {e}"

if __name__ == "__main__":
    # To run this example, ensure you have Google Cloud credentials configured.
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # You can also set GOOGLE_CLOUD_PROJECT for the project_id if not using GOOGLE_APPLICATION_CREDENTIALS directly.
    
    # Example of translating to Spanish
    for translated_caption in live_caption_translator(target_language="es"):
        print(translated_caption)
    
    print("\n")
    
    # Example of translating to French
    for translated_caption in live_caption_translator(target_language="fr"):
        print(translated_caption)
