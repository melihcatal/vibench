from google.cloud import speech

def get_speech_client():
    return speech.SpeechClient()

def get_recognition_config(encoding, sample_rate_hertz, language_code):
    return speech.RecognitionConfig(encoding=encoding, sample_rate_hertz=sample_rate_hertz, language_code=language_code)

def get_streaming_config(recognition_config, interim_results=True):
    return speech.StreamingRecognitionConfig(config=recognition_config, interim_results=interim_results)
