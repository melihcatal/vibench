from google.cloud import texttospeech_v1 as tts
from speech_client import SpeechClient
from speech_models import (
    VoiceSelection,
    SynthesisRequest,
    SynthesisResponse,
    AudioEncoding,
    AudioConfig,
)


def synthesize_ssml(
    ssml: str, language_code: str, voice_name: str = None, **prosody_kwargs
) -> SynthesisResponse:
    client = SpeechClient().get_client()

    voice = VoiceSelection(language_code=language_code, name=voice_name)

    audio_config = AudioConfig(audio_encoding=AudioEncoding.MP3)

    request = SynthesisRequest(ssml=ssml, voice=voice, audio_config=audio_config)

    response = client.synthesize_speech(
        input=tts.SynthesisInput(ssml=request.ssml),
        voice=tts.VoiceSelectionParams(
            language_code=request.voice.language_code, name=request.voice.name
        ),
        audio_config=tts.AudioConfig(
            audio_encoding=request.audio_config.audio_encoding.value,
            speaking_rate=prosody_kwargs.get("speaking_rate"),
            pitch=prosody_kwargs.get("pitch"),
            volume_gain_db=prosody_kwargs.get("volume_gain_db"),
        ),
    )

    return SynthesisResponse(
        audio_content=response.audio_content,
        audio_encoding=request.audio_config.audio_encoding,
    )
