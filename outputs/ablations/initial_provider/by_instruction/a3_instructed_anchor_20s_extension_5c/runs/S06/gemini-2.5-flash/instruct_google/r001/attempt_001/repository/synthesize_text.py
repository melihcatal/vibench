from speech_client import TextToSpeechClient
from speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig, SynthesizeSpeechRequest

def synthesize_text_to_audio(text: str, language_code: str = "en-US", voice_name: str = "en-US-Standard-A", audio_encoding: str = "MP3") -> bytes:
    client = TextToSpeechClient()
    synthesis_input = SynthesisInput(text=text)
    voice_params = VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = AudioConfig(audio_encoding=audio_encoding)
    request = SynthesizeSpeechRequest(input=synthesis_input, voice=voice_params, audio_config=audio_config)
    response = client.synthesize_speech(request)
    return response.audio_content
