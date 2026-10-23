from google.cloud import texttospeech


def generate_audio_preview(
    text: str, language_code: str = "en-US", voice_name: str = "en-US-Wavenet-D"
):
    """
    Generates a spoken audio preview of the given text.

    Args:
        text: The text to synthesize.
        language_code: The language of the text (e.g., 'en-US', 'es-ES').
        voice_name: The specific voice to use for the synthesis.

    Returns:
        The audio content in bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
