from google.cloud import texttospeech
from speech_client import TextToSpeechClientHelper
from speech_models import SynthesisRequest, SynthesisResponse

def synthesize_ssml(payload: dict, config: dict = None) -> dict:
    config = config or {}
    client_helper = TextToSpeechClientHelper()
    client = client_helper.get_client()

    ssml_input = texttospeech.SynthesisInput(ssml=payload["ssml"])
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=config.get("language_code", "en-US"),
        name=config.get("voice_name"),
        ssml_gender=texttospeech.SsmlVoiceGender[config.get("ssml_gender", "NEUTRAL").upper()]
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[config.get("audio_encoding", "MP3").upper()],
        speaking_rate=config.get("speaking_rate"),
        pitch=config.get("pitch"),
        volume_gain_db=config.get("volume_gain_db")
    )

    response = client.synthesize_speech(
        input=ssml_input,
        voice=voice_params,
        audio_config=audio_config
    )

    return SynthesisResponse(audio_bytes=response.audio_content, content_type="audio/mpeg").__dict__
