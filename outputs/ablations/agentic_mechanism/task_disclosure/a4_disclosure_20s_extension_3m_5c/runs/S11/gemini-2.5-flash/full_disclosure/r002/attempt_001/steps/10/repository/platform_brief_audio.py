import os
from google.cloud import texttospeech

def generate_audio_briefing(platform_output: str, output_filename: str = "briefing.mp3"):
    """
    Generates a spoken briefing from platform output using Google Cloud Text-to-Speech.

    Args:
        platform_output: The text content of the briefing.
        output_filename: The name of the file to save the audio to.
    """
    # Instantiates a client using Google Cloud Text-to-Speech
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=platform_output)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
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
        print(f"Audio content written to file: {output_filename}")

if __name__ == "__main__":
    # Example usage:
    example_output = "This is a brief audio summary of the platform's recent activities. Important updates include new deployments and performance enhancements."
    generate_audio_briefing(example_output)
