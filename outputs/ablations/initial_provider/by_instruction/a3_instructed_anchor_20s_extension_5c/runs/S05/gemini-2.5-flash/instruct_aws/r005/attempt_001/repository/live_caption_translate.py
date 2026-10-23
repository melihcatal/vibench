import asyncio
from google.cloud import translate_v3 as translate
from speech_client import SpeechClient
from speech_models import TranscriptResult

async def translate_live_caption(transcript_result: TranscriptResult, target_language_code: str = "es") -> TranscriptResult:
    client = SpeechClient().get_google_translate_client()

    project_id = client.common_project_path(client.project)

    # Google Cloud Translation model identification signal: 'translate_text' method
    response = client.translate_text(
        request={
            "parent": project_id,
            "contents": [transcript_result.transcript],
            "mime_type": "text/plain",  # Mime types: text/plain, text/html
            "source_language_code": transcript_result.language_code or "en-US", # Default to en-US if not specified
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    # Return a new TranscriptResult with the translated text and updated language code
    return TranscriptResult(
        transcript=translated_text,
        is_partial=transcript_result.is_partial,
        start_time=transcript_result.start_time,
        end_time=transcript_result.end_time,
        language_code=target_language_code, # Update to target language
        confidence=transcript_result.confidence
    )

async def simulated_caption_stream(num_captions: int = 3, initial_language: str = "en-US"):
    captions = [
        "Hello, how are you today?",
        "This is an interim result.",
        "Thank you for joining the meeting."
    ]
    for i in range(min(num_captions, len(captions))):
        is_partial = (i < len(captions) - 1)
        yield TranscriptResult(transcript=captions[i], is_partial=is_partial, language_code=initial_language)
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    async def main():
        print("Demonstrating live caption translation using Google Cloud Translation.")
        target_lang = "fr"
        print(f"Translating captions to {target_lang}...")
        async for original_caption in simulated_caption_stream(initial_language="en-US"):
            translated_caption = await translate_live_caption(original_caption, target_language_code=target_lang)
            print(f"Original ({original_caption.language_code}): {original_caption.transcript}")
            print(f"Translated ({translated_caption.language_code}): {translated_caption.transcript}\n")
    asyncio.run(main())
