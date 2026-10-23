from translation_client import get_text_to_speech_client
from translation_models import AudioPreviewRequest
from google.cloud import texttospeech  # Provider-identifying signal


def generate_localized_audio_preview(request: AudioPreviewRequest) -> bytes:
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[request.audio_encoding]
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
