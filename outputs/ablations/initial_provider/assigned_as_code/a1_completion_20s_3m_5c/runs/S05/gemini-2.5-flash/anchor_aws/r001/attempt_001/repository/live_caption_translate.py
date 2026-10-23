from google.cloud import translate_v3 as translate
from typing import AsyncIterable

from speech_models import TranscriptSegment

async def live_caption_translate(transcript_segments: AsyncIterable[TranscriptSegment], target_language_code: str):
    client = translate.TranslationServiceClient()

    # A translation client only needs to be created once and can be reused.
    # Location must be a region for v3. For example, us-central1
    # For a list of available locations, see: 
    # https://cloud.google.com/translate/docs/advanced/locations
    project_id = "your-gcp-project-id"  # Replace with your GCP Project ID
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    async for segment in transcript_segments:
        if segment.text:
            response = client.translate_text(
                request={
                    "parent": parent,
                    "contents": [segment.text],
                    "mime_type": "text/plain",  # Mime types: "text/plain", "text/html"
                    "source_language_code": "en-US",  # Assuming source is English from STT
                    "target_language_code": target_language_code,
                }
            )
            for translation in response.translations:
                translated_text = translation.translated_text
                print(f"Original: {segment.text} -> Translated ({target_language_code}): {translated_text}")
                yield TranscriptSegment(
                    text=translated_text,
                    is_final=segment.is_final,
                    start_time=segment.start_time,
                    end_time=segment.end_time,
                    alternatives=segment.alternatives # Keep original alternatives or process translated ones if needed
                )
