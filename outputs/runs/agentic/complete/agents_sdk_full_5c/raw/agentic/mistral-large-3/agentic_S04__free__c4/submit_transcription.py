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

    job = cloud_speech.CreateRecognizerRequest(
        parent=f"projects/{os.getenv('GOOGLE_PROJECT_ID')}/locations/global",
        recognizer_id="batch-transcriber",
        recognizer=cloud_speech.Recognizer(
            display_name="Batch Transcription Job",
            default_recognition_config=config,
        ),
    )

    operation = client.create_recognizer(request=job)
    recognizer = operation.result()

    long_audio_config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[request.language_code],
        model="latest_long",
    )

    batch_recognize_request = cloud_speech.BatchRecognizeRequest(
        recognizer=recognizer.name,
        config=long_audio_config,
        files=[cloud_speech.BatchRecognizeFileMetadata(uri=request.audio_uri)],
        recognition_output_config=output_config,
    )

    operation = client.batch_recognize(request=batch_recognize_request)
    return operation.operation.name