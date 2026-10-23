from speech_client import TextToSpeechClient
from speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig, SynthesizeSpeechRequest

def synthesize_ssml_to_audio(ssml: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-F", ssml_gender: str = "FEMALE", audio_encoding: str = "MP3") -> bytes:
    client = TextToSpeechClient()
    synthesis_input = SynthesisInput(ssml=ssml)
    voice_params = VoiceSelectionParams(language_code=language_code, name=voice_name, ssml_gender=ssml_gender)
    audio_config = AudioConfig(audio_encoding=audio_encoding)
    request = SynthesizeSpeechRequest(input=synthesis_input, voice=voice_params, audio_config=audio_config)
    response = client.synthesize_speech(request)
    return response.audio_content
