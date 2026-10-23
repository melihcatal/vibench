def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {'text': payload}
    return {'text': payload.get('text', ''), 'locale': payload.get('locale'), 'voice': payload.get('voice')}


def normalize_ssml_payload(payload):
    if isinstance(payload, str):
        return {'ssml': payload}
    return {'ssml': payload.get('ssml', ''), 'voice': payload.get('voice'), 'prosody': payload.get('prosody', {})}


def audio_response(audio_bytes, content_type='audio/mpeg'):
    return {'audio_bytes': audio_bytes, 'content_type': content_type}


def voice_response(voices):
    return {'voices': voices}
