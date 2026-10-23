from speech_client import get_text_to_speech_client
from speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig, SynthesizeSpeechRequest, SynthesizeSpeechResponse
from google.cloud import texttospeech

def synthesize_ssml(ssml_content: str, voice_name: str, language_code: str = "en-US") -> SynthesizeSpeechResponse:
    client = get_text_to_speech_client()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_content)
    voice_params = texttospeech.VoiceSelectionParams(language_code=language_code, name=voice_name)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)

    return SynthesizeSpeechResponse(audio_content=response.audio_content, content_type="audio/mpeg")
