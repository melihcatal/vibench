from google.cloud import texttospeech

def generate_audio_briefing(text: str, output_filepath: str):
    """
    Generates spoken briefings from platform outputs using Google Cloud Text-to-Speech.

    Args:
        text (str): The text content to convert to speech.
        output_filepath (str): The file path to save the generated audio (e.g., "output.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice (e.g., US English, female voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    # Configure the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
