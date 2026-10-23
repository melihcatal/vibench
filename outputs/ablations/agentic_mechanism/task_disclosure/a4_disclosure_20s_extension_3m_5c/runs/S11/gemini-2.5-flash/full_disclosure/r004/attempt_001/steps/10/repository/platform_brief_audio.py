from google.cloud import texttospeech

def generate_spoken_briefing(text_content: str, output_filepath: str = "briefing.mp3"):
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.

    Args:
        text_content: The text to be converted to speech.
        output_filepath: The path to save the generated audio file (e.g., "briefing.mp3").

    Returns:
        The path to the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Select the type of audio file you want to generate
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
