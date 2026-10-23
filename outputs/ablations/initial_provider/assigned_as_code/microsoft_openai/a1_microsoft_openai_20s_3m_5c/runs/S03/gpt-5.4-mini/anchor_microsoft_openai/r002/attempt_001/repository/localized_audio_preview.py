import requests


def localized_audio_preview(payload, config=None):
    config = config or {}
    response = requests.post(
        'https://api.openai.com/v1/audio/speech',
        headers={'Authorization': f"Bearer {config['api_key']}"},
        json={
            'model': 'gpt-4o-mini-tts',
            'input': payload['text'],
            'voice': payload.get('voice', 'alloy')
        },
        timeout=30
    )
    response.raise_for_status()
    return {'audio': response.content}
