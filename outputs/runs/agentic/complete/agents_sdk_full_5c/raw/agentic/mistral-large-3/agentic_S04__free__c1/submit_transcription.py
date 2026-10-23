import os
from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import TranscriptionRequest

def submit_transcription(audio_uri: str, language_code: str = "en-US") -> str:
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text."""
    client = get_speech_client()
    request = TranscriptionRequest(audio_uri=audio_uri, language_code=language_code)

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[request.language_code],
        model="latest_long",
    )

    output_config = cloud_speech.RecognitionOutputConfig(
        gcs_output_config=cloud_speech.GcsOutputConfig(
            uri=os.getenv("GOOGLE_TRANSCRIPT_OUTPUT_URI", "gs://transcript-output-bucket/")
        )
    )

    operation = client.create_recognizer(
        parent=f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/global",
        recognizer_id=f"transcription-job-{os.getenv('GOOGLE_JOB_ID_PREFIX', 'default')}",
        recognizer=cloud_speech.Recognizer(
            default_recognition_config=config,
            output_config=output_config,
        ),
    )

    operation = client.batch_recognize(
        recognizer=operation.result().name,
        config=config,
        files=[cloud_speech.BatchRecognizeFileMetadata(uri=request.audio_uri)],
        recognition_output_config=output_config,
    )

    return operation.name