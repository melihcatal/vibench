import os
from google.cloud import texttospeech
from translation_models import AudioPreviewRequest, AudioPreviewResponse

def generate_localized_audio_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,  # Specific voice name (e.g., 'en-US-Wavenet-D')
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Default gender
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. It can be saved to a file or played.
    return AudioPreviewResponse(audio_content=response.audio_content)
