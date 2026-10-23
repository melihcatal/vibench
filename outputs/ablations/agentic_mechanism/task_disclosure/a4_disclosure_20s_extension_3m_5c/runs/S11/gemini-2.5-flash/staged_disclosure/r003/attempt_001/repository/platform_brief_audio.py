from google.cloud import texttospeech
import os

def generate_spoken_briefing(text_input, output_filename="briefing.mp3"):
    """
    Generates a spoken briefing from text using Google Cloud Text-to-Speech.

    Args:
        text_input (str): The text content for the briefing.
        output_filename (str): The desired filename for the output audio (e.g., "briefing.mp3").
    """

    # Instantiates a client
    # Make sure to set up Google Cloud authentication, e.g., by setting the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For more information, visit:
    # https://cloud.google.com/docs/authentication/getting-started
    client = texttospeech.TextToSpeechClient() # Provider identifiable here

    # Set the synthesis input
    synthesis_input = texttospeech.SynthesisInput(text=text_input)

    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example voice, choose as per preference
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio output
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the audio content to a file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    briefing_text = "This is a sample briefing generated using Google Cloud Text-to-Speech. It provides an overview of recent platform activities and key updates. Stay tuned for more information."
    generate_spoken_briefing(briefing_text, "platform_briefing.mp3")
