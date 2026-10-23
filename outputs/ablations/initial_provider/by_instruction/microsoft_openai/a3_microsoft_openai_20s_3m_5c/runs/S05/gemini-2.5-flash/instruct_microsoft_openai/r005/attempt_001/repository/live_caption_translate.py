import os
from google.cloud import translate_v2 as translate
from typing import AsyncGenerator, Dict, Any

# Google Cloud Translation client setup
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or authenticate appropriately.

async def live_caption_translate(caption_generator: AsyncGenerator[str, None], target_language: str = "es", source_language: str = "en") -> AsyncGenerator[Dict[str, Any], None]:
    client = translate.Client()

    print(f"Starting live caption translation from {source_language} to {target_language} using Google Cloud Translation...")
    print("Please ensure you have authenticated with Google Cloud (e.g., gcloud auth application-default login)")
    print("and enabled the Cloud Translation API.")

    async for caption_chunk in caption_generator:
        if not caption_chunk.strip():
            continue

        try:
            # Google Cloud Translation can automatically detect the source language if not provided.
            # For a real-time scenario, passing the source_language is more efficient.
            translation_result = client.translate(
                caption_chunk,
                target_language=target_language,
                source_language=source_language
            )
            yield {
                "original_text": caption_chunk,
                "translated_text": translation_result["translatedText"],
                "source_language": translation_result.get("detectedSourceLanguage", source_language),
                "target_language": target_language,
            }
        except Exception as e:
            print(f"Error translating caption chunk '{caption_chunk}': {e}")
            # Yield an error or skip, depending on desired error handling
            yield {"error": str(e), "original_text": caption_chunk}

if __name__ == "__main__":
    async def dummy_caption_stream():
        captions = [
            "Hello, how are you today?",
            "This is a test sentence.",
            "I hope this works well.",
            "Goodbye for now."
        ]
        for caption in captions:
            await asyncio.sleep(1)
            yield caption

    async def main():
        print("Running live caption translation example.")
        async for result in live_caption_translate(dummy_caption_stream(), target_language="fr"):
            if "translated_text" in result:
                print(f"Original: {result['original_text']} -> Translated ({result['target_language']}): {result['translated_text']}")
            elif "error" in result:
                print(f"Translation error for '{result['original_text']}': {result['error']}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Translation stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
