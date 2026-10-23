from google.cloud import texttospeech

def synthesize_ssml(ssml_text, voice_name="en-US-Wavenet-D", speaking_rate=1.0, pitch=0.0):
    """
    Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.

    Args:
        ssml_text (str): The SSML text to synthesize.
        voice_name (str): The name of the voice to use (e.g., "en-US-Wavenet-D").
        speaking_rate (float): The speaking rate (0.25 to 4.0). 1.0 is the normal natural pace.
        pitch (float): The pitch of the synthesized voice. -20.0 to 20.0.

    Returns:
        bytes: The audio content in MP3 format.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="-".join(voice_name.split("-")[:2]),
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
