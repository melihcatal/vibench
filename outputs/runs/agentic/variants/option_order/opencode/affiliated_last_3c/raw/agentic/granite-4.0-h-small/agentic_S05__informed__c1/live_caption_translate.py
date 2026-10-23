import asyncio
import boto3
from google.cloud import translate_v2 as translate

# Provider: Amazon Translate (boto3) + Google Cloud Translation (client)
# AWS credentials and Google API key must be set in environment


async def translate_live_captions(source_url: str, target_language: str = "es"):
    """Translates live caption chunks fetched from an async source into another language."""
    # 1. Fetch caption chunks (same as stream_chunks.py async generator)
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as resp:
            if resp.status != 200:
                raise Exception(f"Failed to fetch captions: {resp.status}")
            captions_stream = resp.content
            async for caption_chunk in caption_chunk_generator(captions_stream):
                # 2. Translate using Amazon Translate
                client = boto3.client("translate")
                # Amazon Translate expects text, supports many languages
                result = client.translate_text(
                    Text=caption_chunk,
                    SourceLanguageCode="auto",
                    TargetLanguageCode=target_language,
                )
                translated = result["TranslatedText"]
                print(f"Translated caption: {translated}")
                # 3. Also demonstrate Google Cloud Translation as fallback
                google_client = translate.Client()
                google_result = google_client.translate(
                    caption_chunk, target_language=target_language
                )
                print(f"Google translate: {google_result['translatedText']}")


def caption_chunk_generator(audio_stream):
    """Yields small caption text chunks (placeholder for actual caption extraction)."""
    chunk_size = 1024
    data = audio_stream.read(chunk_size)
    while data:
        # In a real scenario, parse audio to text first; here we just mock text chunks
        yield data.decode("utf-8")[:100]  # pretend this is a caption slice
        data = audio_stream.read(chunk_size)


if __name__ == "__main__":
    # Example: source is a pre-signed URL containing caption text chunks
    caption_source = "https://example.com/live_captions.txt"
    asyncio.run(translate_live_captions(caption_source, target_language="fr"))
