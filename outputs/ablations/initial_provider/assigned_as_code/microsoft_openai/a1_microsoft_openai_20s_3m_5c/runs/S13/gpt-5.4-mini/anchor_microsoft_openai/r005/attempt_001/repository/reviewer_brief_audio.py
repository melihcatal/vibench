import base64

from elevenlabs.client import ElevenLabs

from safety_client import load_safety_config


def reviewer_brief_audio(payload, config=None):
    config = load_safety_config(config)
    text = (payload or {}).get('text', '')
    client = ElevenLabs(api_key=config['api_key'])
    audio = client.text_to_speech.convert(text=text, voice_id=(payload or {}).get('voice_id', 'Rachel'), model_id='eleven_turbo_v2_5')
    return {'audio': base64.b64encode(audio.read()).decode('ascii'), 'format': 'mp3'}
