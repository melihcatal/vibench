import asyncio
import os
from google.cloud import translate_v2 as translate

from speech_models import TranscriptionResult


async def translate_caption_chunk(text: str, target_language: str = "es"):
    """
    Translates a caption chunk to the target language using Google Cloud Translation.
    """
    translate_client = translate.Client()

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print(
            "WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
            "Translation may fail if not authenticated."
        )

    try:
        result = translate_client.translate(text, target_language=target_language)
        return result["translatedText"]
    except Exception as e:
        print(f"Error during translation: {e}")
        return None


async def live_caption_translate(
    caption_stream_async_generator, target_language: str = "es"
):
    """
    Translates live captions from an async generator.
    """
    async for caption_event in caption_stream_async_generator:
        if caption_event["is_final"]:
            translated_text = await translate_caption_chunk(
                caption_event["transcript"], target_language
            )
            if translated_text:
                yield {
                    "original": caption_event["transcript"],
                    "translated": translated_text,
                }
            else:
                yield {
                    "original": caption_event["transcript"],
                    "translated": "[Translation Failed]",
                }
        else:
            # Optionally yield partial translations or just original partials
            yield {
                "original": caption_event["transcript"],
                "translated": "[Partial - not translated]",
            }


if __name__ == "__main__":

    async def dummy_caption_source():
        # Simulate a stream of transcription results
        await asyncio.sleep(1)
        yield {"transcript": "Hello, how are you today?", "is_final": False}
        await asyncio.sleep(1)
        yield {
            "transcript": "Hello, how are you today? I hope you are doing well.",
            "is_final": True,
        }
        await asyncio.sleep(1)
        yield {"transcript": "This is another sentence.", "is_final": False}
        await asyncio.sleep(1)
        yield {
            "transcript": "This is another sentence. It is a final one.",
            "is_final": True,
        }

    async def main():
        print("Starting live caption translation...")
        try:
            async for translated_caption in live_caption_translate(
                dummy_caption_source(), target_language="fr"
            ):
                print(
                    f"Original: {translated_caption['original']} -> Translated: {translated_caption['translated']}"
                )
        except KeyboardInterrupt:
            print("\nStopped live caption translation.")

    asyncio.run(main())
