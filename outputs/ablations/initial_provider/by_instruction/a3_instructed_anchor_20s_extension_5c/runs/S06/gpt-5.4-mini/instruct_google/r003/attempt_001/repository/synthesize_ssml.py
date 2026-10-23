from google.cloud import texttospeech

from speech_client import get_audio_encoding, get_client, get_default_language_code, get_default_voice_name
from speech_models import AudioResult, SSMLRequest, normalize_ssml


def synthesize_ssml(ssml: str) -> AudioResult:
    request = SSMLRequest(ssml=normalize_ssml(ssml), language_code=get_default_language_code(), voice_name=get_default_voice_name())
    client = get_client()
    synthesis_input = texttospeech.SynthesisInput(ssml=request.ssml)
    voice = texttospeech.VoiceSelectionParams(language_code=request.language_code, name=request.voice_name) if request.voice_name else texttospeech.VoiceSelectionParams(language_code=request.language_code)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=texttospeech.AudioConfig(audio_encoding=get_audio_encoding()))
    return AudioResult(audio_content=response.audio_content, voice_name=request.voice_name)
