from google.cloud import speech_v1p1beta1 as speech

def create_streaming_config(language_code, enable_automatic_punctuation):
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    return speech.types.StreamingRecognitionConfig(config=config, interim_results=True)