from google.cloud.speech import enums

def normalize_response(response):
    return [{'text': result.alternatives[0].transcript, 'is_final': result.is_final} for result in response.results]
