
from google.cloud import texttospeech
import os

# Google Cloud Text-to-Speech client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
# authenticate your application using other methods.
# For more information, see:
# https://cloud.google.com/docs/authentication/getting-started

def generate_spoken_briefing(text: str, output_filename: str = "briefing.mp3"):
    """
    Generates a spoken briefing from the given text using Google Cloud Text-to-Speech.

    Args:
        text (str): The text to be converted to speech.
        output_filename (str): The name of the output audio file (e.g., "briefing.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    # You can explore available voices here: https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    briefing_text = """
    Good morning. Here is your daily platform briefing.
    All systems are operational.
    There was a 10% increase in user activity over the last 24 hours.
    New deployments for feature X are scheduled for tomorrow.
    """
    generate_spoken_briefing(briefing_text, "platform_briefing.mp3")
