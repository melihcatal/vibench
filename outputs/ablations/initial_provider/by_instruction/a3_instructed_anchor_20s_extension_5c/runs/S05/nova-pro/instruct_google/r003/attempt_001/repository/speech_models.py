from google.cloud import speech

def create_streaming_config(language_code='en-US', enable_automatic_punctuation=True):
    config = {
        'encoding': speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        'sample_rate_hertz': 16000,
        'language_code': language_code,
        'enable_automatic_punctuation': enable_automatic_punctuation,
    }
    return speech.types.StreamingRecognitionConfig(config=config, interim_results=True)