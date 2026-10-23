from google.cloud import texttospeech

def generate_spoken_brief(text: str) -> bytes:
    """Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.

    Args:
        text: The text content of the brief.

    Returns:
        Audio data in bytes.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content
