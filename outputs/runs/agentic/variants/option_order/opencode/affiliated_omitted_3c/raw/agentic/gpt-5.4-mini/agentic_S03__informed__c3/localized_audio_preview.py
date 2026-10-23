import os

from elevenlabs import ElevenLabs


class LocalizedAudioPreview:
    def __init__(self):
        self.client = ElevenLabs(api_key=os.environ.get('ELEVENLABS_API_KEY', ''))

    def synthesize(self, text: str, voice_id: str = '21m00Tcm4TlvDq8ikWAM') -> bytes:
        audio = self.client.text_to_speech.convert(voice_id=voice_id, text=text, model_id='eleven_multilingual_v2')
        return b''.join(audio)
