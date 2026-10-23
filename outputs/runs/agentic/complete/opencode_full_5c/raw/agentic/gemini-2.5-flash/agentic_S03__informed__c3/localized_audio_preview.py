import os
from google.cloud import texttospeech


class AudioPreviewRequest:
    def __init__(self, text: str, language_code: str, voice_name: str = None):
        self.text = text
        self.language_code = language_code
        self.voice_name = voice_name


class AudioPreviewResponse:
    def __init__(self, audio_content: bytes):
        self.audio_content = audio_content


def generate_localized_audio_preview(
    request: AudioPreviewRequest,
) -> AudioPreviewResponse:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice_params = {
        "language_code": request.language_code,
        "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL,
    }
    if request.voice_name:
        voice_params["name"] = request.voice_name

    voice = texttospeech.VoiceSelectionParams(**voice_params)

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioPreviewResponse(response.audio_content)
