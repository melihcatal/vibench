from google.cloud import texttospeech_v1
from speech_client import get_speech_client
from speech_models import SSMLVoiceConfig

def synthesize_ssml_to_audio(ssml: str, voice_config: SSMLVoiceConfig) -> bytes:
    """
    Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.
    """
    client = get_speech_client()
    
    input_ssml = texttospeech_v1.SynthesisInput(ssml=ssml)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=voice_config.language_code,
        name=voice_config.voice_name
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3,
        speaking_rate=voice_config.speaking_rate,
        pitch=voice_config.pitch
    )
    
    response = client.synthesize_speech(
        input=input_ssml, voice=voice, audio_config=audio_config
    )
    
    return response.audio_content