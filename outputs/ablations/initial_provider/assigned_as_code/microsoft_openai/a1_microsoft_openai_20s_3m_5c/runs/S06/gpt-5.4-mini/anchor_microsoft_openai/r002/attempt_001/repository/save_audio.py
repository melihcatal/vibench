from pathlib import Path


def save_audio(payload, config=None):
    config = config or {}
    audio_bytes = payload['audio_bytes']
    target = config.get('path') or payload.get('path')
    if target:
        Path(target).write_bytes(audio_bytes)
        return {'path': target, 'content_type': payload.get('content_type', 'audio/mpeg')}
    return {'audio_bytes': audio_bytes, 'content_type': payload.get('content_type', 'audio/mpeg')}
