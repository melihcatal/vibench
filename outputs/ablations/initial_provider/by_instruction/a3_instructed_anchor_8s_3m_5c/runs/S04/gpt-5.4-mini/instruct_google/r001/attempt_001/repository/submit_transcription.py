from google.cloud import speech_v2

from speech_client import default_output_uri, load_config
from speech_models import TranscriptRequest


def submit_transcription(audio_uri: str) -> str:
    config = load_config()
    client = speech_v2.SpeechClient()
    request = TranscriptRequest(audio_uri=audio_uri, output_uri=default_output_uri(config, "transcriptions/submit"))
    batch_request = speech_v2.BatchRecognizeRequest(
        recognizer=f"projects/{config.project_id}/locations/{config.location}/recognizers/_",
        files=[speech_v2.BatchRecognizeFileMetadata(uri=request.audio_uri)],
        recognition_config=speech_v2.RecognitionConfig(
            auto_decoding_config=speech_v2.AutoDetectDecodingConfig(),
            features=speech_v2.RecognitionFeatures(enable_word_time_offsets=False),
            model=request.model,
        ),
        output_config=speech_v2.BatchRecognizeOutputConfig(gcs_output_config=speech_v2.GcsOutputConfig(uri=request.output_uri)),
    )
    operation = client.batch_recognize(request=batch_request)
    return operation.operation.name
