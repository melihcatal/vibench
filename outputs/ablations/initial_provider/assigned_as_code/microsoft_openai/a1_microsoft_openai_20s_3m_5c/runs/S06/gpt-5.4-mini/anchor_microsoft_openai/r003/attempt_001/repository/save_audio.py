from pathlib import Path

from speech_client import load_tts_config, synthesize_text_with_config


def save_audio(payload, config=None):
    config = load_tts_config(config)
    audio = payload.get('audio_bytes')
    if audio is None and payload.get('text'):
        audio = synthesize_text_with_config(payload['text'], config)
    path = payload.get('path')
    if path:
        Path(path).write_bytes(audio)
        return {'path': path, 'content_type': 'audio/mpeg'}
    return {'audio_bytes': audio, 'content_type': 'audio/mpeg'}
