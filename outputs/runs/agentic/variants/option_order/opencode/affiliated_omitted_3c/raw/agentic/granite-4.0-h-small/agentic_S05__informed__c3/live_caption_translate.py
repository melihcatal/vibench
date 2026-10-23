# live_caption_translate.py
# [LATER-STEP]
# Translate live captions into another language using DeepL API

import asyncio
import json
import os
import sys
import deepgram  # also used for streaming source (optional)
import deepl  # DeepL client

# Load credentials from environment
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY", "${DEEPL_AUTH_KEY}")
SOURCE_LANG = "en"  # default source language (override with env var if needed)
TARGET_LANG = "es"  # default target language (override with env var if needed)

# Initialize DeepL client
translator = deepl.Translator(auth_key=DEEPL_AUTH_KEY)


async def translate_live_captions(
    captions: asyncio.Queue,  # Queue of interim/final caption strings
    output_queue: asyncio.Queue,  # Queue for translated results as dict: {original, translated}
):
    async for caption in captions:
        # Skip empty captions
        if not caption:
            continue
        try:
            # Translate using DeepL (text limit 5000 chars; split if needed)
            translation = await asyncio.to_thread(
                translator.translate_text,
                text=caption,
                source_lang=SOURCE_LANG,
                target_lang=TARGET_LANG,
            )
            output_queue.put_nowait({"original": caption, "translated": translation})
        except Exception as exc:
            print("Translation error:", exc)


async def run_translation_pipeline(
    recognizer: deepgram.client.StreamingRecognizer,  # Deepgram streaming recognizer instance
    captions_queue: asyncio.Queue,
    translation_queue: asyncio.Queue,
):
    # Feed recognizer results into captions queue (interim results)
    async for caption in recognizer.interim_results():
        # Each item is a dict with a 'results' list; extract first transcript
        transcript = (
            recognizer.extract_latest_transcript(caption)
            if hasattr(recognizer, "extract_latest_transcript")
            else extract_transcript_from_deepgram(caption)
        )
        if transcript:
            captions_queue.put_nowait(transcript)

    # Optionally you could also handle final results here


async def main():
    # 1. Set up Deepgram streaming recognizer (same as stream_microphone or stream_with_language)
    client = deepgram.client.Client(DEEPGRAM_API_KEY)
    recognizer = client.streaming_recognize(
        model="nvidia_large", language="en", punctuate=False, interim_results=True
    )

    # 2. Create queues for communication between tasks
    captions = asyncio.Queue()
    translated = asyncio.Queue()

    # 3. Start translation worker
    asyncio.create_task(translate_live_captions(captions, translated))

    # 4. Run recognition and feed captions
    await recognizer.start()
    async for caption in recognizer:
        # This yields each partial result as a dict; we forward the raw JSON string for demo
        captions.put_nowait(caption)

    # When you stop recognition, you can collect remaining translations
    await recognizer.stop()
    # Drain translation queue
    while not translated.empty():
        print("Translated:", await translated.get())

    await recognizer.close()


# Helper to extract transcript from Deepgram raw result dict (fallback for async loop)


def extract_transcript_from_deepgram(result: Dict[str, Any]) -> str:
    try:
        return result["results"][0]["alternatives"][0]["transcript"]
    except (KeyError, IndexError, TypeError):
        return ""


if __name__ == "__main__":
    # Example CLI usage: python live_caption_translate.py <audio_file.wav>
    # For demo, we run a dummy recognizer that reads a local WAV file (requires pyaudio & .wav)
    import sys

    audio_path = sys.argv[1] if len(sys.argv) > 1 else "sample.wav"
    # Start the async pipeline
    asyncio.run(main())
