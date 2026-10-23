from google.cloud import speech_v1p1beta1 as speech

def create_config(language_code='en-US'):
    return speech.types.RecognitionConfig(encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                                           sample_rate_hertz=16000,
                                           language_code=language_code,
                                           enable_automatic_punctuation=True)

def create_streaming_config(config):
    return speech.types.StreamingRecognitionConfig(config=config)