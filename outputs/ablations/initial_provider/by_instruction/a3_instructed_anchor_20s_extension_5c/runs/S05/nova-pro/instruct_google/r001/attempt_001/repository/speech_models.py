from google.cloud import speech

def recognition_config(language_code='en-US', sample_rate_hertz=16000):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )
    return config

def streaming_recognition_config(config):
    streaming_config = speech.StreamingRecognitionConfig(config=config)
    return streaming_config