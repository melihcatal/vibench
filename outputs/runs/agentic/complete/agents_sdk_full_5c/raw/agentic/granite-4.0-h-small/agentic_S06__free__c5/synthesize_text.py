# synthesize_text.py
# [SAME-SCENARIO] Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

from google.cloud import texttospeech
from speech_client import get_texttospeech_client

def synthesize_text(text: str, language_code: str = 'en-US', voice_name: str = None) -> bytes:
    """Synthesize plain text to audio bytes.

    Args:
        text: The plain text to synthesize.
        language_code: BCP-47 language tag.
        voice_name: Optional specific voice name (e.g., 'en-US-Wavenet-D').

    Returns:
        Raw audio bytes (default format: MP3).
    """
    client = get_texttospeech_client()
    # Build the voice request
    if voice_name:
        voice = texttospeech.VoiceSelectionParams(name=voice_name)
    else:
        voice = texttospeech.VoiceSelectionParams(language_code=language_code)
    # Select default SSML voice gender and speaking rate
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    # Create the synthesize request
    synthesis_input = texttospeech.SynthesisInput(text=text)
    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # Perform synthesis
    response = client.synthesize_speech(request=request)
    # Return raw audio content as bytes
    return response.audio_content
