from translation_client import get_text_to_speech_client
from translation_models import (
    LocalizedAudioPreviewRequest,
    LocalizedAudioPreviewResponse,
)
from google.cloud import texttospeech


def generate_localized_audio_preview(
    request: LocalizedAudioPreviewRequest,
) -> LocalizedAudioPreviewResponse:
    client = get_text_to_speech_client()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    # Build the voice request, select the language code (e.g., "en-US") and the ssml
    # voice gender (optional)
    voice_params = {"language_code": request.language_code}
    if request.voice_name:
        voice_params["name"] = request.voice_name
    voice = texttospeech.VoiceSelectionParams(**voice_params)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        request=texttospeech.SynthesizeSpeechRequest(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
    )

    # The audio_content is binary. You can save it to a file or stream it.
    return LocalizedAudioPreviewResponse(audio_content=response.audio_content)
