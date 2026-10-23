from google.cloud import texttospeech_v1
from speech_client import get_speech_client
from speech_models import SSMLVoiceConfig

def synthesize_text_to_audio(text: str, language_code: str = "en-US", voice_name: str = None) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.
    """
    client = get_speech_client()
    
    if voice_name is None:
        voice_name = f"{language_code[:2]}-Wavenet-D"
    
    input_text = texttospeech_v1.SynthesisInput(text=text)
    voice = texttospeech_v1.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )
    
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    
    return response.audio_content