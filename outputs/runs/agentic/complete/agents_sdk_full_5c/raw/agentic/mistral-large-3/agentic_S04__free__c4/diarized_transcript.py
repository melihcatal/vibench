import os
from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import DiarizedTranscriptionRequest, DiarizedTranscriptionResult

def diarized_transcript(audio_uri: str, language_code: str = "en-US") -> DiarizedTranscriptionResult:
    """Request speaker diarization for a recorded meeting using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    request = DiarizedTranscriptionRequest(audio_uri=audio_uri, language_code=language_code)

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[request.language_code],
        model="latest_long",
        features=cloud_speech.RecognitionFeatures(
            enable_speaker_diarization=True,
            diarization_speaker_count=2,
        ),
    )

    output_config = cloud_speech.RecognitionOutputConfig(
        gcs_output_config=cloud_speech.GcsOutputConfig(
            uri=os.getenv("GOOGLE_DIARIZED_OUTPUT_URI", "gs://diarized-output-bucket/")
        )
    )

    recognizer_name = f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/global/recognizers/_"

    batch_recognize_request = cloud_speech.BatchRecognizeRequest(
        recognizer=recognizer_name,
        config=config,
        files=[cloud_speech.BatchRecognizeFileMetadata(uri=request.audio_uri)],
        recognition_output_config=output_config,
    )

    operation = client.batch_recognize(request=batch_recognize_request)
    operation.result()

    # Fetch results from GCS
    from google.cloud import storage
    storage_client = storage.Client()
    bucket_name, blob_path = output_config.gcs_output_config.uri[5:].split("/", 1)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_path + "transcript.json")
    results = cloud_speech.BatchRecognizeResults.from_json(
        blob.download_as_text(), ignore_unknown_fields=True
    )

    segments = []
    for result in results.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                segments.append({
                    "speaker_tag": word_info.speaker_tag,
                    "word": word_info.word,
                    "start_time": word_info.start_offset.total_seconds(),
                    "end_time": word_info.end_offset.total_seconds(),
                })

    return DiarizedTranscriptionResult(segments=segments)