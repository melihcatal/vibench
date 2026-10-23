from google.cloud import texttospeech

from speech_client import get_audio_encoding, get_client, get_default_language_code, get_default_voice_name
from speech_models import AudioResult, TextRequest, normalize_text


def synthesize_text(text: str) -> AudioResult:
    request = TextRequest(text=normalize_text(text), language_code=get_default_language_code(), voice_name=get_default_voice_name())
    client = get_client()
    synthesis_input = texttospeech.SynthesisInput(text=request.text)
    voice = texttospeech.VoiceSelectionParams(language_code=request.language_code, name=request.voice_name) if request.voice_name else texttospeech.VoiceSelectionParams(language_code=request.language_code)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=texttospeech.AudioConfig(audio_encoding=get_audio_encoding()))
    return AudioResult(audio_content=response.audio_content, voice_name=request.voice_name)
