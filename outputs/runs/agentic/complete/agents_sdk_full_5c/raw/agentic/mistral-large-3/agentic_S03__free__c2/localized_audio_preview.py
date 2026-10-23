from typing import Optional
import boto3
from translation_models import TranslationResponse

class LocalizedAudioPreviewGenerator:
    def __init__(self):
        self.client = boto3.client(service_name='polly', region_name='us-east-1')

    def generate_audio_preview(self, text: str, language_code: str, voice_id: Optional[str] = None) -> bytes:
        voice_map = {
            'en': 'Joanna',
            'es': 'Lucia',
            'fr': 'Lea',
            'de': 'Marlene'
        }
        selected_voice = voice_id or voice_map.get(language_code[:2], 'Joanna')

        response = self.client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId=selected_voice,
            LanguageCode=language_code
        )
        return response['AudioStream'].read()