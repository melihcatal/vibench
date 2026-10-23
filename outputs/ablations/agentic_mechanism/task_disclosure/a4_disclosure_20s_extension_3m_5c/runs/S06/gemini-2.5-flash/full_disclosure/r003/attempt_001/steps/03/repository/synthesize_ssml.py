from google.cloud import texttospeech

def synthesize_ssml(ssml_text, voice_name, language_code, audio_encoding, speaking_rate=1.0, pitch=0.0):
    """Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech.

    Args:
        ssml_text: The SSML input text to be synthesized.
        voice_name: The name of the voice to use (e.g., "en-US-Standard-C").
        language_code: The language code for the voice (e.g., "en-US").
        audio_encoding: The desired audio encoding (e.g., "MP3", "LINEAR16").
        speaking_rate: The speaking rate (1.0 is normal, 0.5 is half, 2.0 is double).
        pitch: The pitch of the synthesized voice (in semitones, +20 to -20).

    Returns:
        The audio content bytes.
    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Default to neutral, can be extended if needed
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, audio_encoding),
        speaking_rate=speaking_rate,
        pitch=pitch,
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    return response.audio_content

