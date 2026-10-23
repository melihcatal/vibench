from google.cloud.speech_v1 import enums

def normalize_response(response):
    return {
        'transcript': response.results[0].alternatives[0].transcript,
        'is_final': response.results[0].is_final,
    }