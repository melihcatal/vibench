from speech_client import get_speech_client
from speech_models import TranscriptionRequest
from google.cloud import speech_v1p1beta1 as speech


def submit_diarized_transcription(audio_uri: str, language_code: str = "en-US") -> str:
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16, user might need to adjust
        sample_rate_hertz=16000,  # Assuming 16000 Hz, user might need to adjust
        language_code=language_code,
        enable_automatic_punctuation=True,
        enable_speaker_diarization=True,
        diarization_config=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True, min_speaker_count=2, max_speaker_count=6
        ),  # Example diarization config
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.operation.name
