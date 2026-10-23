from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    SynthesizeSpeechRequest,
    SynthesizeSpeechResponse,
)


def synthesize_text_to_audio(
    text: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Standard-A",
    audio_encoding: str = "MP3",
) -> SynthesizeSpeechResponse:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config_params = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[audio_encoding]
    )

    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice_params, audio_config=audio_config_params
    )

    response = client.synthesize_speech(request=request)
    return SynthesizeSpeechResponse(audio_content=response.audio_content)
