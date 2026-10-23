from google.cloud import texttospeech

def synthesize_text_to_audio(text: str, voice_name: str = "en-US-Standard-A", audio_encoding: texttospeech.AudioEncoding = texttospeech.AudioEncoding.MP3) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        voice_name: The name of the voice to use for synthesis (e.g., "en-US-Standard-A").
        audio_encoding: The audio encoding for the output (e.g., MP3, LINEAR16).

    Returns:
        A bytes object containing the audio content.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=texttospeech.VoiceSelectionParams(name=voice_name), audio_config=audio_config
    )

    return response.audio_content
