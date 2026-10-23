from speech_client import get_tts_client
from speech_models import SpeechSynthesisRequest, SpeechSynthesisResponse
from google.cloud import texttospeech


def synthesize_ssml(request: SpeechSynthesisRequest) -> SpeechSynthesisResponse:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.language_code, name=request.voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return SpeechSynthesisResponse(audio_content=response.audio_content)
