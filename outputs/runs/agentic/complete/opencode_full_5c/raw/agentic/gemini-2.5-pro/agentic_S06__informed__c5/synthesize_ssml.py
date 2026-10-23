from speech_client import get_speech_client
from speech_models import SpeechRequest, SynthesizeResponse
from google.cloud import texttospeech


def synthesize_ssml(request: SpeechRequest) -> SynthesizeResponse:
    """
    Synthesizes speech from SSML.
    The SSML input should be in the `text` field of the request.
    """
    client = get_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=request.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code,
        name=request.voice if request.voice else "en-US-Wavenet-D",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return SynthesizeResponse(audio_content=response.audio_content, request=request)
