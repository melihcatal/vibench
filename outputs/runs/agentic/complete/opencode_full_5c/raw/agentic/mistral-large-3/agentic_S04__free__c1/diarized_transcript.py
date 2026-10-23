from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import SpeechModels, TranscriptionResult


def diarized_transcript(audio_file_path: str) -> TranscriptionResult:
    """Request speaker diarization for a recorded meeting using Google Cloud Speech-to-Text."""
    diarization_config = types.SpeakerDiarizationConfig(
        enable_speaker_diarization=True, min_speaker_count=2, max_speaker_count=10
    )

    config = TranscriptionConfig(diarization_config=diarization_config)
    client_helper = SpeechClient(config)
    client = client_helper.get_client()

    audio = client_helper.load_audio(audio_file_path)
    recognition_config = client_helper.create_recognition_config()

    operation = client.long_running_recognize(config=recognition_config, audio=audio)
    operation.result()

    response = types.LongRunningRecognizeResponse.from_json(operation.response)
    return SpeechModels.normalize_response(response)
