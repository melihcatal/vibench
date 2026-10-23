from google.cloud import speech_v1p1beta1 as speech
from google.protobuf import duration_pb2

def submit_transcription_job(gcs_uri: str, audio_channel_count: int = 1, language_code: str = "en-US"):
    """
    Submits an audio file for batch transcription using Google Cloud Speech-to-Text API.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        audio_channel_count: The number of channels in the audio file.
        language_code: The language of the supplied audio (e.g., "en-US").

    Returns:
        The operation name of the long-running transcription job.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code=language_code,
        audio_channel_count=audio_channel_count,
        enable_automatic_punctuation=True,
    )

    # Configure the long-running operation
    operation = client.long_running_recognize(config=config, audio=audio)

    return operation.operation.name
