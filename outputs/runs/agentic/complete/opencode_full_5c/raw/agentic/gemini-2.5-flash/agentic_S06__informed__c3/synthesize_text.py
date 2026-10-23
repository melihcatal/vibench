from speech_client import get_tts_client
from speech_models import SynthesisRequest
from google.cloud import texttospeech


def synthesize_text(request: SynthesisRequest) -> bytes:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.text)

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=request.voice_config.language_code,
        name=request.voice_config.name,
        ssml_gender=texttospeech.SsmlVoiceGender[request.voice_config.ssml_gender],
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[request.audio_encoding]
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice_selection_params, audio_config=audio_config
    )

    return response.audio_content
