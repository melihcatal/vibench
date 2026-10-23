import os
from google.cloud import texttospeech

def generate_audio_briefing(text_input, output_filename="briefing.mp3"):
    """
    Generates an audio briefing from the given text using Google Cloud Text-to-Speech.

    Args:
        text_input (str): The text to be converted to speech.
        output_filename (str): The name of the output MP3 file.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text_input)

    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Using a Wavenet voice for high quality
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to an MP3 file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file {output_filename}")

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    
    briefing_text = """
    Good morning. Here is your daily platform briefing.
    All systems are operational.
    There were 12 new deployments in the last 24 hours with no critical errors reported.
    Current resource utilization is at 60%, which is within normal operating parameters.
    One security alert was generated but has been resolved.
    Have a productive day.
    """
    generate_audio_briefing(briefing_text, "platform_briefing.mp3")
