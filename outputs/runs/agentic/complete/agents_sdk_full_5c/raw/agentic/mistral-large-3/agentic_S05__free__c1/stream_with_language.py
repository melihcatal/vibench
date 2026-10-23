from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

def start_stream_with_language(language_code="en-US", enable_punctuation=True):
    client = SpeechClient()
    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language_code],
        model="latest_long",
        features=cloud_speech.RecognitionFeatures(
            enable_automatic_punctuation=enable_punctuation,
            enable_spoken_punctuation=True,
            enable_spoken_emojis=True,
        ),
    )
    return client.streaming_recognize(
        config=config,
        streaming_config=cloud_speech.StreamingRecognitionConfig(
            config=config,
            streaming_features=cloud_speech.StreamingRecognitionFeatures(
                interim_results=True
            ),
        ),
    )