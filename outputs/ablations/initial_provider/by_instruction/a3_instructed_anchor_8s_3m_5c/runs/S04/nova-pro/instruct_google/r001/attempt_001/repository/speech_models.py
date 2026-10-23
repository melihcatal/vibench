from google.cloud import speech_v1 as speech

def normalize_response(response):
    transcript = ' '.join([result.alternatives[0].transcript for result in response.results])
    return transcript