from google.cloud import speech

def create_config(encoding, sample_rate, language_code):
    return speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate,
        language_code=language_code,
    )

def create_streaming_config(config, interim_results=True):
    return speech.StreamingRecognitionConfig(config=config, interim_results=interim_results)