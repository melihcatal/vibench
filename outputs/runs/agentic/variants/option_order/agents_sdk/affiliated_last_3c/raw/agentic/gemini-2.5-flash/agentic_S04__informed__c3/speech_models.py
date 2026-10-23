from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

def create_recognition_config(
    encoding: enums.RecognitionConfig.AudioEncoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    enable_speaker_diarization: bool = False,
    diarization_speaker_count: int = 0,
    enable_word_time_offsets: bool = False,
) -> speech.types.RecognitionConfig:
    """
    Creates a Google Cloud Speech-to-Text RecognitionConfig object.
    """
    return speech.types.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_speaker_diarization=enable_speaker_diarization,
        diarization_speaker_count=diarization_speaker_count,
        enable_word_time_offsets=enable_word_time_offsets,
    )

def create_recognition_audio(gcs_uri: str) -> speech.types.RecognitionAudio:
    """
    Creates a Google Cloud Speech-to-Text RecognitionAudio object from a GCS URI.
    """
    return speech.types.RecognitionAudio(uri=gcs_uri)
