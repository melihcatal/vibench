from speech_client import get_speech_client
from speech_models import SynthesisRequest, SynthesizedSpeech
from google.cloud import texttospeech


def synthesize_text(request: SynthesisRequest) -> SynthesizedSpeech:
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return SynthesizedSpeech(audio_content=response.audio_content)
