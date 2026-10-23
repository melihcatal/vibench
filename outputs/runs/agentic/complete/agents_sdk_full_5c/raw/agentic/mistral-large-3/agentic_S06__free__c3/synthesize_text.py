from google.cloud import texttospeech_v1 as tts
from speech_client import get_speech_client
from speech_models import SynthesisRequest, SynthesisResponse

def synthesize_text(text: str, voice_name: str = "en-US-Standard-A", language_code: str = "en-US") -> SynthesisResponse:
    client = get_speech_client()
    input_data = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.MP3
    )
    request = SynthesisRequest(
        input=input_data,
        voice=voice,
        audio_config=audio_config
    )
    response = client.synthesize_speech(
        request=input_data,
        voice=voice,
        audio_config=audio_config
    )
    return SynthesisResponse(audio_content=response.audio_content)