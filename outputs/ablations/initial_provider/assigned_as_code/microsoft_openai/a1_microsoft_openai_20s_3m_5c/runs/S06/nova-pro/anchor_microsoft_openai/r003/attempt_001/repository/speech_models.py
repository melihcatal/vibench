def normalize_payload(payload):
    if 'text' in payload:
        payload['text'] = payload['text'].strip()
    if 'ssml' in payload:
        payload['ssml'] = payload['ssml'].strip()
    return payload

def normalize_response(response):
    if 'audio_bytes' in response:
        response['audio_bytes'] = response['audio_bytes'].strip()
    return response