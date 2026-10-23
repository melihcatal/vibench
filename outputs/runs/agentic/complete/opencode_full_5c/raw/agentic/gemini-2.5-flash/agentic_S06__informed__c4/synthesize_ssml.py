from speech_client import TextToSpeechClient
from speech_models import (
    SynthesisInput,
    VoiceSelectionParams,
    AudioConfig,
    SynthesizeSpeechRequest,
)


def synthesize_ssml(
    ssml: str, voice_name: str, language_code: str, audio_encoding: str = "MP3"
) -> bytes:
    client = TextToSpeechClient()
    synthesis_input = SynthesisInput(ssml=ssml)
    voice_params = VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = AudioConfig(audio_encoding=audio_encoding)

    request = SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice_params, audio_config=audio_config
    )

    audio_content = client.synthesize_speech(request)
    return audio_content
