"""
Translate completed transcript segments using Google Cloud Translation API.

Provider: Google Cloud Translation API v3
SDK: google-cloud-translate
Endpoint: translation.googleapis.com
Environment: GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
"""

from typing import List, Optional, Dict, Any

from google.cloud import translate_v3 as translate

from speech_models import TranscriptSegment


def translate_segments(
    segments: List[TranscriptSegment],
    target_language: str = "es",
    source_language: Optional[str] = None,
    project_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate transcript segments to a target language.

    Args:
        segments: List of TranscriptSegment objects to translate
        target_language: Target language code (BCP-47, e.g., 'es', 'fr', 'de')
        source_language: Source language code, or None for auto-detect
        project_id: Google Cloud project ID

    Returns:
        List of dicts with original and translated text per segment.
    """
    if project_id is None:
        import os
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT is not set")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    contents = [seg.transcript for seg in segments]

    request = translate.TranslateTextRequest(
        contents=contents,
        target_language_code=target_language,
        parent=parent,
        source_language_code=source_language or "",
        mime_type="text/plain",
    )

    response = client.translate_text(request=request)

    translated = []
    for i, translation in enumerate(response.translations):
        translated.append({
            "segment_index": i,
            "original_text": segments[i].transcript,
            "original_language": translation.detected_language_code if translation.detected_language_code else source_language,
            "translated_text": translation.translated_text,
            "target_language": target_language,
            "confidence": segments[i].confidence,
            "speaker_tag": segments[i].speaker_tag,
        })

    return translated


def translate_full_transcript(
    segments: List[TranscriptSegment],
    target_language: str = "es",
    project_id: Optional[str] = None,
) -> str:
    """
    Translate the full combined transcript text.

    Returns the complete translated transcript as a string.
    """
    full_text = " ".join(seg.transcript for seg in segments)

    if project_id is None:
        import os
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    request = translate.TranslateTextRequest(
        contents=[full_text],
        target_language_code=target_language,
        parent=parent,
        mime_type="text/plain",
    )

    response = client.translate_text(request=request)
    return response.translations[0].translated_text


def batch_translate_documents(
    gcs_source_uri: str,
    gcs_target_uri: str,
    source_language: str,
    target_language: str,
    project_id: Optional[str] = None,
) -> str:
    """
    Batch translate transcription output files stored in GCS.

    Uses Google Cloud Translation batch processing for large documents.

    Args:
        gcs_source_uri: GCS URI of source text file
        gcs_target_uri: GCS URI for translated output
        source_language: Source language code
        target_language: Target language code
        project_id: Google Cloud project ID

    Returns:
        Operation name for the batch translation job.
    """
    if project_id is None:
        import os
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    gcs_source = translate.GcsSource(input_uri=gcs_source_uri)
    input_config = translate.InputConfig(
        gcs_source=gcs_source,
        mime_type="text/plain",
    )

    gcs_destination = translate.GcsDestination(output_uri_prefix=gcs_target_uri)
    output_config = translate.OutputConfig(gcs_destination=gcs_destination)

    request = translate.BatchTranslateTextRequest(
        parent=parent,
        source_language_code=source_language,
        target_language_codes=[target_language],
        input_configs=[input_config],
        output_config=output_config,
    )

    operation = client.batch_translate_text(request=request)
    return operation.operation.name


if __name__ == "__main__":
    import sys

    print("Usage: Import translate_transcript and use with transcription results.")
    print("Example:")
    print("  from translate_transcript import translate_segments")
    print("  translated = translate_segments(segments, target_language='es')")
    print("  for t in translated:")
    print("      print(f\"{t['original_text']} -> {t['translated_text']}\")")
