from google.cloud import speech


def get_speech_client():
    return speech.SpeechClient()


def get_recognition_config(sample_rate_hz, language_code):
    return speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz, language_code=language_code)


def get_streaming_config(recognition_config):
    return speech.StreamingRecognitionConfig(config=recognition_config, interim_results=True)