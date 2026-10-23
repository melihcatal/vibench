from google.cloud import speech_v1p1beta1 as speech

def create_speech_config(language_code, encoding, sample_rate_hertz):
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding(encoding),
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code
    )
    return config

def create_audio(content):
    audio = speech.types.RecognitionAudio(content=content)
    return audio

def normalize_response(response):
    results = []
    for result in response.results:
        alternative = result.alternatives[0]
        results.append(alternative.transcript)
    return results