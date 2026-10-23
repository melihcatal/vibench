import os
from google.cloud import texttospeech

def generate_spoken_briefing(text_input, output_filename="briefing.mp3"):
    """
    Generates a spoken briefing from text using Google Cloud Text-to-Speech.

    Args:
        text_input (str): The text to be converted to speech.
        output_filename (str): The name of the output audio file.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_input)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example platform output (replace with actual integration)
    platform_output = "The latest platform briefing indicates a stable system performance with no critical alerts. All services are operating within normal parameters. There are no pending updates."
    generate_spoken_briefing(platform_output)
