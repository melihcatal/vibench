import os
from elevenlabs import generate, save
from translation_models import AudioPreviewRequest


def localized_audio_preview(request: AudioPreviewRequest) -> str:
    """
    Generates a spoken preview of translated copy using ElevenLabs.
    Returns the file path to the generated audio.
    """
    api_key = os.environ.get("ELEVENLABS_API_KEY")

    audio = generate(
        text=request.text,
        voice=request.voice_id,
        api_key=api_key,
        model="eleven_multilingual_v2",
    )

    output_path = "localized_preview.mp3"
    save(audio, output_path)

    return output_path
