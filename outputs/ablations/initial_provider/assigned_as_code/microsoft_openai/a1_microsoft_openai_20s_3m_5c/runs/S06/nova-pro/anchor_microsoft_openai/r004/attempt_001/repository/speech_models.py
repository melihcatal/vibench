from azure.cognitiveservices.speech import SpeechSynthesisOutputFormat


def normalize_payload(payload):
    if 'voice' in payload:
        payload['voice'] = payload['voice'].replace(' ', '')
    return payload


def parse_response(response):
    return {'audio_bytes': response.audio_data, 'content_type': 'audio/mpeg'}
