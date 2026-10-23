from speech_client import get_tts_client
from speech_models import SynthesisRequest, SynthesisResponse, VoiceConfig, AudioConfig
from google.cloud import texttospeech

def synthesize_ssml(request: SynthesisRequest) -> SynthesisResponse:
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=request.voice.language_code,
        name=request.voice.name,
        ssml_gender=request.voice.ssml_gender
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, request.audio_config.audio_encoding),
        speaking_rate=request.audio_config.speaking_rate,
        pitch=request.audio_config.pitch,
        volume_gain_db=request.audio_config.volume_gain_db,
        sample_rate_hertz=request.audio_config.sample_rate_hertz
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config
    )

    return SynthesisResponse(audio_content=response.audio_content)
