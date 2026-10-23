from google.cloud import texttospeech_v1
from speech_client import get_speech_client
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_ssml(ssml: str, voice_name: str = "en-US-Standard-A", language_code: str = "en-US") -> SynthesisResponse:
    """Synthesize SSML with voice and prosody controls using Google Cloud Text-to-Speech."""
    client = get_speech_client()
    
    input_data = texttospeech_v1.SynthesisInput(ssml=ssml)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )
    
    request = SynthesisRequest(
        input=input_data,
        voice=voice,
        audio_config=audio_config
    )
    
    response = client.synthesize_speech(
        request=request.input,
        voice=request.voice,
        audio_config=request.audio_config
    )
    
    return SynthesisResponse(audio_content=response.audio_content)