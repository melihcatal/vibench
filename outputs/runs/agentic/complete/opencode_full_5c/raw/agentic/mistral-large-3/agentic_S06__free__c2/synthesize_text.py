from google.cloud import texttospeech_v1 as tts
from speech_client import SpeechClient
from speech_models import (
    VoiceSelection,
    SynthesisRequest,
    SynthesisResponse,
    AudioEncoding,
)


def synthesize_text(
    text: str, language_code: str, voice_name: str = None
) -> SynthesisResponse:
    client = SpeechClient().get_client()

    voice = VoiceSelection(language_code=language_code, name=voice_name)

    request = SynthesisRequest(
        text=text,
        voice=voice,
        audio_config=AudioConfig(audio_encoding=AudioEncoding.MP3),
    )

    response = client.synthesize_speech(
        input=tts.SynthesisInput(text=request.text),
        voice=tts.VoiceSelectionParams(
            language_code=request.voice.language_code, name=request.voice.name
        ),
        audio_config=tts.AudioConfig(
            audio_encoding=request.audio_config.audio_encoding.value
        ),
    )

    return SynthesisResponse(
        audio_content=response.audio_content,
        audio_encoding=request.audio_config.audio_encoding,
    )
