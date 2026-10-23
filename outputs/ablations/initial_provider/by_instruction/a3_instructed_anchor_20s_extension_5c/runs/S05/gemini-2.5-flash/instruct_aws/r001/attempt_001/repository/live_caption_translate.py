import asyncio
from google.cloud import translate

async def live_caption_translate(caption_stream_async_generator, target_language_code="es"):
    """
    Translates live caption chunks from an async source into another language
    using Google Cloud Translation API.

    Args:
        caption_stream_async_generator: An async generator that yields caption strings.
        target_language_code (str): The BCP-47 language tag for the target language (e.g., "es" for Spanish).
    """
    client = translate.TranslationServiceClient()
    # Project ID is usually picked up from GOOGLE_APPLICATION_CREDENTIALS or environment.
    # For explicit project, use: project_id = "your-project-id"
    # parent = f"projects/{project_id}"

    print(f"Translating live captions to '{target_language_code}' using Google Cloud Translation...")

    async for caption in caption_stream_async_generator:
        if not caption.strip():
            continue

        try:
            response = client.translate_text(
                contents=[caption],
                target_language_code=target_language_code,
                # parent=parent, # Uncomment if using explicit project_id
                mime_type="text/plain",  # Mime types: "text/plain" or "text/html"
            )
            for translation in response.translations:
                yield {"original": caption, "translated": translation.translated_text, "language": target_language_code}
        except Exception as e:
            print(f"Error during translation: {e}")
            yield {"original": caption, "translated": f"Error: {e}", "language": target_language_code}

if __name__ == "__main__":
    async def mock_caption_generator():
        yield "Hello world, how are you today?"
        await asyncio.sleep(1)
        yield "This is a test sentence for translation."
        await asyncio.sleep(1)
        yield "Live captions can be very helpful."

    async def main():
        print("Translating captions to Spanish:")
        async for result in live_caption_translate(mock_caption_generator(), target_language_code="es"):
            print(f"Original: {result["original"]} -> Translated ({result["language"]}: {result["translated"]})")

        print("\nTranslating captions to German:")
        async for result in live_caption_translate(mock_caption_generator(), target_language_code="de"):
            print(f"Original: {result["original"]} -> Translated ({result["language"]}: {result["translated"]})")

    asyncio.run(main())
