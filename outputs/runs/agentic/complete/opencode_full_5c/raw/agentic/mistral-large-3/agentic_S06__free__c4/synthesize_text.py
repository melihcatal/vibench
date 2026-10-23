from google.cloud import texttospeech_v1 as texttospeech
from speech_client import SpeechClient
from speech_models import VoiceSelection, AudioConfig, AudioEncoding, SynthesisResponse


def synthesize_text(
    text: str,
    language_code: str,
    voice_name: str = None,
    audio_encoding: AudioEncoding = AudioEncoding.MP3,
) -> SynthesisResponse:
    client = SpeechClient().get_client()

    voice = VoiceSelection(language_code=language_code, name=voice_name)

    audio_config = AudioConfig(audio_encoding=audio_encoding)

    input_text = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=voice.language_code, name=voice.name
    )
    audio_params = texttospeech.AudioConfig(audio_encoding=audio_encoding.value)

    response = client.synthesize_speech(
        input=input_text, voice=voice_params, audio_config=audio_params
    )

    return SynthesisResponse(
        audio_content=response.audio_content, audio_config=audio_config
    )
