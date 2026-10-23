import os
from google.cloud import speech_v2 as speech
from google.cloud.speech_v2.types import cloud_speech
from speech_client import get_speech_client
from speech_models import TranscriptionRequest

def submit_transcription(audio_uri: str, language_code: str = "en-US") -> str:
    """Submit an audio file for batch transcription using Google Cloud Speech-to-Text."""
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

    file_metadata = cloud_speech.BatchRecognizeFileMetadata(
        uri=request.audio_uri,
        config=config,
    )

    operation = client.batch_recognize(
        request={
            "recognizer": f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/global/recognizers/_",
            "files": [file_metadata],
            "output_config": output_config,
        }
    )
    return operation.operation.name