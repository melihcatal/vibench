from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client, get_audio_config, SpeechConfig
from speech_models import TranscriptionResult, normalize_response


def timestamped_transcript(audio_uri: str) -> TranscriptionResult:
    """Return word or segment timestamps from a Google Cloud Speech-to-Text transcription result."""
    client = get_speech_client()
    config = SpeechConfig(enable_word_time_offsets=True)
    audio_config = get_audio_config(config, audio_uri)
    recognition_audio = types.RecognitionAudio(uri=audio_uri)

    operation = client.long_running_recognize(
        config=audio_config,
        audio=recognition_audio,
    )

    operation.result()
    return normalize_response(operation.result())
