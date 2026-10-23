import asyncio
from google.cloud import translate_v3 as translate

async def translate_text_async(project_id: str, target_language_code: str, text_content: str) -> str:
    """Translates a given text asynchronously using Google Cloud Translation API."""
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided for translation.")

    client = translate.TranslationServiceClient()
    location = "global" # Or a specific region, e.g., "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    response = await asyncio.to_thread( # Use to_thread for blocking API calls in async context
        client.translate_text,
        request={
            "parent": parent,
            "contents": [text_content],
            "target_language_code": target_language_code,
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
        }
    )

    # The response can contain multiple translations, but for a single input text, we expect one.
    if response.translations:
        return response.translations[0].translated_text
    return ""

async def live_caption_translate_pipeline(caption_stream, project_id: str, target_language: str):
    """Simulates a live caption translation pipeline."""
    print(f"\n--- Live Caption Translation Pipeline (to {target_language}) ---")
    async for original_transcript, is_final in caption_stream:
        if original_transcript.strip():
            translated_text = await translate_text_async(project_id, target_language, original_transcript)
            status = "(Final)" if is_final else "(Partial)"
            print(f"Original {status}: {original_transcript}")
            print(f"Translated {status}: {translated_text}")
            yield original_transcript, translated_text, is_final

async def mock_caption_stream():
    """A mock async generator for caption chunks."""
    yield "Hello world", False
    await asyncio.sleep(0.5)
    yield "How are you doing today?", True
    await asyncio.sleep(1)
    yield "This is a test of live translation.", False
    await asyncio.sleep(0.7)
    yield "I hope it works well.", True

async def main():
    # Replace with your actual Google Cloud Project ID
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    import os
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id-here")

    if project_id == "your-gcp-project-id-here":
        print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Using placeholder.")
        print("Translation will not work without a valid project ID.")

    async for original, translated, is_final in live_caption_translate_pipeline(
        mock_caption_stream(), 
        project_id, 
        "es" # Translate to Spanish
    ):
        pass # The pipeline function already prints.

if __name__ == "__main__":
    asyncio.run(main())
