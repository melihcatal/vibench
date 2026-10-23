from google.cloud import speech

# Define local request, response, and normalization helpers for Streaming Speech-to-Text

def create_streaming_config(language_code='en-US'):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    return speech.StreamingRecognitionConfig(config=config)

def normalize_response(response):
    for result in response.results:
        for alternative in result.alternatives:
            yield alternative.transcript