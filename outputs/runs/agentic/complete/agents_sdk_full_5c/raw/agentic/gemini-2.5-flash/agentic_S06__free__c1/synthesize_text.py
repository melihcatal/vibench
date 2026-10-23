import os
from google.cloud import texttospeech

def synthesize_plain_text(text: str, voice_name: str, language_code: str, output_format: str = "MP3") -> bytes:
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-A").
        language_code: The BCP-47 language code (e.g., "en-US").
        output_format: The audio output format (e.g., "MP3", "LINEAR16").

    Returns:
        The audio content as bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding[output_format],
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
