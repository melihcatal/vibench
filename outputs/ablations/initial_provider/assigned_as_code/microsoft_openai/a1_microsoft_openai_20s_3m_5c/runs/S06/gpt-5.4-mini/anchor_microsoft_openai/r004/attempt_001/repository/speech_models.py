def normalize_text_payload(payload):
    if isinstance(payload, str):
        return {'text': payload}
    return {'text': payload.get('text', ''), 'ssml': payload.get('ssml')}


def normalize_voice_request(payload, config=None):
    config = dict(config or {})
    if isinstance(payload, str):
        payload = {'locale': payload}
    config['locale'] = payload.get('locale', config.get('locale', 'en-US'))
    config['voice'] = payload.get('voice', config.get('voice'))
    return config


def parse_audio_result(result):
    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
