from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import SsmlSynthesisRequest, AudioResponse


def synthesize_ssml(request: SsmlSynthesisRequest) -> AudioResponse:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    if request.voice:
        voice.name = request.voice.name

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return AudioResponse(audio_content=response.audio_content)
