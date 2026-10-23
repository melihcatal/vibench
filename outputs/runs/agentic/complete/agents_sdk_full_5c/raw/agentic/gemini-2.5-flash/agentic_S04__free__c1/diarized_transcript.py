from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client

def request_diarized_transcript(gcs_uri: str, audio_channel_count: int = 1, enable_speaker_diarization: bool = True, min_speaker_count: int = 1, max_speaker_count: int = 6):
    client = get_speech_client()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Example
        sample_rate_hertz=16000, # Example
        language_code="en-US",
        audio_channel_count=audio_channel_count,
        enable_automatic_punctuation=True,
        diarization_config=speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=enable_speaker_diarization,
            min_speaker_count=min_speaker_count,
            max_speaker_count=max_speaker_count,
        ),
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    # The operation name can be used to poll the result later.
    return operation.operation.name
