from translation_client import elevenlabs_client
from translation_models import AudioPreviewRequest, AudioPreviewResponse


def localized_audio_preview(request: AudioPreviewRequest) -> AudioPreviewResponse:
    """
    Generates a spoken preview of translated copy using ElevenLabs.
    """
    audio_data = elevenlabs_client.generate(
        text=request.text, voice=request.voice_id, model="eleven_multilingual_v2"
    )
    return AudioPreviewResponse(audio_data=b"".join(audio_data))
