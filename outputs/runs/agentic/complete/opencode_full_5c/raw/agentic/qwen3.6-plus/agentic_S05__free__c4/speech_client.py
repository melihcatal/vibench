import os
from typing import Optional

from google.cloud.speech_v2 import SpeechClient
from google.api_core.client_options import ClientOptions


GOOGLE_SPEECH_API_ENDPOINT = "speech.googleapis.com"
DEFAULT_LOCATION = "global"
DEFAULT_MODEL = "latest_long"


def get_credentials_path() -> Optional[str]:
    return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")


def create_speech_client(
    location: str = DEFAULT_LOCATION,
    credentials_path: Optional[str] = None,
) -> SpeechClient:
    creds = credentials_path or get_credentials_path()
    if creds:
        options = ClientOptions(
            api_endpoint=GOOGLE_SPEECH_API_ENDPOINT,
            credentials_file=creds,
        )
    else:
        options = ClientOptions(api_endpoint=GOOGLE_SPEECH_API_ENDPOINT)
    return SpeechClient(client_options=options)


def build_recognizer_name(
    project_id: str,
    location: str = DEFAULT_LOCATION,
) -> str:
    return f"projects/{project_id}/locations/{location}/recognizers/_"


def build_audio_config(
    sample_rate_hertz: int = 16000,
    encoding: str = "LINEAR16",
    audio_channel_count: int = 1,
) -> dict:
    from google.cloud.speech_v2.types import cloud_speech

    encoding_map = {
        "LINEAR16": cloud_speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "MULAW": cloud_speech.RecognitionConfig.AudioEncoding.MULAW,
        "ALAW": cloud_speech.RecognitionConfig.AudioEncoding.ALAW,
        "MP3": cloud_speech.RecognitionConfig.AudioEncoding.MP3,
        "OGG_OPUS": cloud_speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        "WEBM_OPUS": cloud_speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
    }
    return {
        "auto_decoding_config": {},
        "explicit_decoding_config": cloud_speech.RecognitionConfig.ExplicitDecodingConfig(
            encoding=encoding_map.get(
                encoding, cloud_speech.RecognitionConfig.AudioEncoding.LINEAR16
            ),
            sample_rate_hertz=sample_rate_hertz,
            audio_channel_count=audio_channel_count,
        ),
    }


def build_streaming_config(
    project_id: str,
    model: str = DEFAULT_MODEL,
    language_code: str = "en-US",
    location: str = DEFAULT_LOCATION,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    profanity_filter: bool = False,
    max_alternatives: int = 1,
) -> dict:
    from google.cloud.speech_v2.types import cloud_speech

    recognizer = build_recognizer_name(project_id, location)

    features = cloud_speech.RecognitionFeatures(
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
        profanity_filter=profanity_filter,
        max_alternatives=max_alternatives,
    )

    config = cloud_speech.RecognitionConfig(
        model=model,
        language_codes=[language_code],
        features=features,
    )

    return {
        "recognizer": recognizer,
        "config": config,
        "streaming_features": cloud_speech.StreamingRecognitionFeatures(
            interim_results=True,
            voice_activity_timeout=cloud_speech.StreamingRecognitionFeatures.VoiceActivityTimeout(
                speech_start_timeout="5s",
                speech_end_timeout="3s",
            ),
        ),
    }
