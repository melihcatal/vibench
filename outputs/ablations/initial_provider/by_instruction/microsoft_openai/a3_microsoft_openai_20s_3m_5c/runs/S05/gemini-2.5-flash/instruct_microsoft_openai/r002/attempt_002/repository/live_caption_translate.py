import asyncio
import os
from google.cloud import translate_v2 as translate
from speech_models import LiveCaption

async def translate_live_caption(caption: LiveCaption, target_language: str) -> LiveCaption:
    """Translates a live caption into a target language using Google Cloud Translation API."""
    translate_client = translate.Client()

    # Google Cloud Translation API expects text for translation
    result = translate_client.translate(
        caption.text, 
        target_language=target_language
    )

    translated_text = result['translatedText']
    print(f"Translated '{caption.text}' ({caption.language}) to '{translated_text}' ({target_language})")
    
    return LiveCaption(
        text=translated_text,
        language=target_language,
        is_partial=caption.is_partial
    )

async def main():
    # Set your Google Cloud credentials environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    print("Translating example live captions...")
    example_caption_en = LiveCaption(text="Hello, how are you?", language="en", is_partial=True)
    example_caption_es = LiveCaption(text="¿Cómo estás?", language="es", is_partial=False)

    translated_to_es = await translate_live_caption(example_caption_en, "es")
    translated_to_en = await translate_live_caption(example_caption_es, "en")

    print(f"Translated English caption to Spanish: {translated_to_es.text}")
    print(f"Translated Spanish caption to English: {translated_to_en.text}")

if __name__ == "__main__":
    asyncio.run(main())
