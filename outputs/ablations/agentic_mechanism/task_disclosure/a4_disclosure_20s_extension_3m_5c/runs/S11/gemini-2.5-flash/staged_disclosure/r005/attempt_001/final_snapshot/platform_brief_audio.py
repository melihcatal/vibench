import os
from google.cloud import texttospeech

def generate_audio_briefing(text_content: str, output_filename: str = "briefing.mp3"):
    """
    Generates an audio briefing from the given text content using Google Cloud Text-to-Speech.

    Args:
        text_content: The text to be converted to speech.
        output_filename: The name of the output audio file (e.g., "briefing.mp3").
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_content)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Concrete model identifier
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Ensure you have authenticated with Google Cloud, e.g., by setting the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For more info: https://cloud.google.com/docs/authentication/getting-started
    
    # Placeholder for platform output
    platform_output = "Today's briefing: All systems are nominal. No critical alerts have been detected in the last 24 hours. Enjoy your day."
    generate_audio_briefing(platform_output)
