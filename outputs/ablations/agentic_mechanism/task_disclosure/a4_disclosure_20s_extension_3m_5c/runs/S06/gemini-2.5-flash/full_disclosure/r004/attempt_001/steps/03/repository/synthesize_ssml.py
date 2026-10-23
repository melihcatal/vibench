from google.cloud import texttospeech_v1 as texttospeech

def synthesize_ssml(ssml_text: str, voice_name: str = "en-US-Wavenet-D", speaking_rate: float = 1.0) -> bytes:
    """
    Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.

    Args:
        ssml_text: The SSML input to be synthesized.
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-D").
        speaking_rate: The speaking rate, where 1.0 is normal.

    Returns:
        The audio content as a bytes object.
    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    voice_selection = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice_selection,
        audio_config=audio_config
    )

    return response.audio_content
