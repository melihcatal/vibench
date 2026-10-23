from google.cloud import speech


def speech_client():
    return speech.SpeechClient()


def streaming_config(encoding, sample_rate, language_code, enable_automatic_punctuation=False):
    return speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=encoding,
            sample_rate_hertz=sample_rate,
            language_code=language_code,
            enable_automatic_punctuation=enable_automatic_punctuation),
        interim_results=True)