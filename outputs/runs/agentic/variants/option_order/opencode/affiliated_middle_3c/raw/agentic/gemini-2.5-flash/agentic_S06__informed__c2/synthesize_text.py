from speech_client import get_text_to_speech_client
from speech_models import (
    SynthesisInput,
    VoiceSelection,
    AudioConfig,
    SynthesizeSpeechRequest,
    SynthesizeSpeechResponse,
)
from google.cloud import texttospeech


def synthesize_text(request: SynthesizeSpeechRequest) -> SynthesizeSpeechResponse:
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(text=request.input.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=request.voice.language_code,
        name=request.voice.name,
        ssml_gender=getattr(
            texttospeech.SsmlVoiceGender, request.voice.ssml_gender.upper()
        )
        if request.voice.ssml_gender
        else None,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(
            texttospeech.AudioEncoding, request.audio_config.audio_encoding.upper()
        ),
        speaking_rate=request.audio_config.speaking_rate,
        pitch=request.audio_config.pitch,
        volume_gain_db=request.audio_config.volume_gain_db,
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )

    return SynthesizeSpeechResponse(audio_content=response.audio_content)
