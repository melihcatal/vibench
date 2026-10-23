from google.cloud import texttospeech


def get_client():
    return texttospeech.TextToSpeechClient()


def normalize_payload(payload):
    if 'text' in payload:
        payload['text'] = payload['text'].strip()
    if 'ssml' in payload:
        payload['ssml'] = payload['ssml'].strip()
    return payload