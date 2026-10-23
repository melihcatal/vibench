from google.cloud import speech_v1p1beta1 as speech

def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client instance."""
    return speech.SpeechClient()

def get_recognition_config(rate, language_code="en-US", enable_automatic_punctuation=True):
    """Returns a Google Cloud Speech-to-Text RecognitionConfig."""
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

def get_streaming_config(config, interim_results=True):
    """Returns a Google Cloud Speech-to-Text StreamingRecognitionConfig."""
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )
