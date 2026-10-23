from google.cloud import speech

def create_recognition_config(encoding, sample_rate_hertz, language_code, enable_automatic_punctuation=False, model='default'):
    return speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
    )

def create_streaming_config(recognition_config, interim_results=True):
    return speech.StreamingRecognitionConfig(config=recognition_config, interim_results=interim_results)
