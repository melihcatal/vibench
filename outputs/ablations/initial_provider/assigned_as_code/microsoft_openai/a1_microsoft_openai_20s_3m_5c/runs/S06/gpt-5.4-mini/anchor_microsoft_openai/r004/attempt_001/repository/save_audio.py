def save_audio(payload, config=None):
    config = config or {}
    path = config.get('path') or payload.get('path')
    audio_bytes = payload['audio_bytes']
    if path:
        with open(path, 'wb') as handle:
            handle.write(audio_bytes)
        return {'path': path, 'content_type': payload.get('content_type', 'audio/mpeg')}
    return {'audio_bytes': audio_bytes, 'content_type': payload.get('content_type', 'audio/mpeg')}
