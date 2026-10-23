import os
from elevenlabs.client import ElevenLabs

def platform_brief_audio(text: str):
    client = ElevenLabs(api_key=os.environ['ELEVENLABS_API_KEY'])
    return client.text_to_speech.convert(text=text, voice_id=os.getenv('ELEVENLABS_VOICE_ID', 'JBFqnCBsd6RMkjVDRZzb'), model_id=os.getenv('ELEVENLABS_MODEL_ID', 'eleven_multilingual_v2'))
