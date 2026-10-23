from google.cloud import speech

def get_speech_client():
    return speech.SpeechClient()

def get_streaming_config(sample_rate_hertz, language_code, interim_results=True, enable_automatic_punctuation=False):
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    return speech.StreamingRecognitionConfig(config=recognition_config, interim_results=interim_results)
