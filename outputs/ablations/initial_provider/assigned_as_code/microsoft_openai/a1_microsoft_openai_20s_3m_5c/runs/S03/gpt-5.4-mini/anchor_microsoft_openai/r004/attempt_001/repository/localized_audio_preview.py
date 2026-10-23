import requests

from translation_client import load_translation_config


def localized_audio_preview(payload, config=None):
    config = load_translation_config(config)
    response = requests.post(
        'https://api.openai.com/v1/audio/speech',
        headers={'Authorization': 'Bearer ' + config['api_key'], 'Content-Type': 'application/json'},
        json={'model': 'gpt-4o-mini-tts', 'voice': payload.get('voice', 'alloy'), 'input': payload['text']},
        timeout=config['timeout'],
    )
    response.raise_for_status()
    return {'audio': response.content, 'text': payload['text']}
