from typing import List
import boto3
from translation_models import TranslationResponse

class LocalizedAudioPreview:
    def __init__(self):
        self.client = boto3.client(service_name='polly', region_name='us-east-1')

    def generate_audio_preview(
        self, 
        translations: List[TranslationResponse],
        output_format: str = 'mp3'
    ) -> List[bytes]:
        audio_previews = []
        
        for translation in translations:
            response = self.client.synthesize_speech(
                Text=translation.translated_text,
                OutputFormat=output_format,
                VoiceId='Joanna',  # AWS Polly voice
                LanguageCode=translation.target_lang
            )
            
            audio_previews.append(response['AudioStream'].read())
        
        return audio_previews