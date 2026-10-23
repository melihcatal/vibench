import os
import io
from google.cloud import texttospeech_v1 as tts
from translation_models import AudioPreviewRequest, AudioPreviewResponse

class LocalizedAudioPreviewGenerator:
    def __init__(self):
        self.client = tts.TextToSpeechClient.from_service_account_json(
            os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
        )

    def generate_audio_preview(
        self, 
        text: str, 
        language_code: str, 
        voice_name: str = None
    ) -> bytes:
        synthesis_input = tts.SynthesisInput(text=text)
        voice = tts.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name or f"{language_code}-Standard-A"
        )
        audio_config = tts.AudioConfig(
            audio_encoding=tts.AudioEncoding.MP3
        )
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        return response.audio_content

def generate_localized_audio_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    generator = LocalizedAudioPreviewGenerator()
    audio_content = generator.generate_audio_preview(
        text=request.text,
        language_code=request.language_code,
        voice_name=request.voice_name
    )
    return AudioPreviewResponse(
        audio_content=audio_content,
        format="mp3"
    )