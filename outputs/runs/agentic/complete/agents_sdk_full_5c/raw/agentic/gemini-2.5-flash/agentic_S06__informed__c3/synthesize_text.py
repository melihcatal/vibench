from google.cloud import texttospeech
from speech_client import get_tts_client
from speech_models import VoiceConfig, AudioConfig

def synthesize_plain_text(text: str, voice_config: VoiceConfig, audio_config: AudioConfig) -> bytes:
    """
    Synthesizes plain text into audio bytes using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        voice_config: Configuration for the voice.
        audio_config: Configuration for the audio output.

    Returns:
        Audio content as bytes.
    """
    client = get_tts_client()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_config.language_code,
        name=voice_config.name,
        ssml_gender=getattr(texttospeech.SsmlVoiceGender, voice_config.ssml_gender) if voice_config.ssml_gender else None
    )

    audio_encoding = getattr(texttospeech.AudioEncoding, audio_config.audio_encoding)
    
    audio_configuration = texttospeech.AudioConfig(
        audio_encoding=audio_encoding,
        speaking_rate=audio_config.speaking_rate,
        pitch=audio_config.pitch,
        volume_gain_db=audio_config.volume_gain_db,
        sample_rate_hertz=audio_config.sample_rate_hertz
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_configuration
    )

    return response.audio_content
