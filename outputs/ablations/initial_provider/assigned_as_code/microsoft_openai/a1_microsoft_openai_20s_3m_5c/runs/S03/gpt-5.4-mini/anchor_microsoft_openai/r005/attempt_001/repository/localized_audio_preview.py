from translation_client import load_translation_config


def localized_audio_preview(payload, config=None):
    cfg = load_translation_config(config)
    return {'voice': payload.get('voice', 'en-US-JennyNeural'), 'provider': 'microsoft-azure-text-to-speech', 'region': cfg['region'], 'text': payload['text']}
