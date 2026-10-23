from google.cloud import texttospeech_v1 as tts
from speech_client import get_speech_client
from speech_models import SynthesisInput

def synthesize_ssml_to_audio(ssml: str, voice_name: str = "en-US-Wavenet-D") -> bytes:
    client = get_speech_client()
    input_data = SynthesisInput(ssml=ssml)
    voice = tts.VoiceSelectionParams(
        language_code=voice_name.split("-")[0] + "-" + voice_name.split("-")[1],
        name=voice_name
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)
    request = tts.SynthesizeSpeechRequest(
        input=input_data.to_proto(),
        voice=voice,
        audio_config=audio_config
    )
    response = client.synthesize_speech(request=request)
    return response.audio_content