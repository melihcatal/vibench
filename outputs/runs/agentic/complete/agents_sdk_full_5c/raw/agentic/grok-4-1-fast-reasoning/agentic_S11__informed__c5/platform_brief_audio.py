import os
from elevenlabs.client import ElevenLabs
from elevenlabs.commons import save

def platform_brief_audio(text: str, voice: str = 'Rachel', output_file: str = 'briefing.mp3') -> str:
    api_key = os.getenv('ELEVENLABS_API_KEY')
    if not api_key:
        raise ValueError('ELEVENLABS_API_KEY not set')
    client = ElevenLabs(api_key=api_key)
    audio = client.generate(
        text=text,
        voice=voice,
        model='eleven_multilingual_v2',
        output_format='mp3_44100_128'
    )
    save(audio, output_file)
    return output_file
