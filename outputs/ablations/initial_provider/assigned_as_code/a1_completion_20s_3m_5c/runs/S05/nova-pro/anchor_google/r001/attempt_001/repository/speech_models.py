from google.cloud import speech

def create_streaming_config(language_code='en-US', enable_automatic_punctuation=True):
    config = speech.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)
    return streaming_config

def create_audio_content(audio_data):
    return speech.types.RecognitionAudio(content=audio_data)