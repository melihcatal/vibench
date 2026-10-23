from google.cloud import texttospeech
import os
from translation_models import AudioPreviewRequest, AudioPreviewResponse

def generate_localized_audio_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, 
        name=request.voice_name # e.g., 'en-US-Wavenet-D', 'cmn-CN-Standard-A'
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, request.audio_encoding)
    )
    
    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )
    
    return AudioPreviewResponse(audio_content=response.audio_content)
