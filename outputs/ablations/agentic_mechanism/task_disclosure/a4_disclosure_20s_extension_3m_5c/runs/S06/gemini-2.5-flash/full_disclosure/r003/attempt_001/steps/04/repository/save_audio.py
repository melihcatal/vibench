
import os
from google.cloud import texttospeech

def save_audio_to_file(audio_content: bytes, filename: str):
    """
    Saves the synthesized audio content to a local file.

    Args:
        audio_content: The audio content as bytes.
        filename: The name of the file to save the audio to.
    """
    try:
        with open(filename, "wb") as out:
            out.write(audio_content)
        print(f"Audio content written to file: {filename}")
    except IOError as e:
        print(f"Error writing audio to file {filename}: {e}")

def synthesize_and_save_audio(text: str, filename: str, voice_name: str = "en-US-Wavenet-C", language_code: str = "en-US"):
    """
    Synthesizes speech from text using Google Cloud Text-to-Speech and saves it to a file.

    Args:
        text: The text to synthesize.
        filename: The name of the file to save the audio to.
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-C").
        language_code: The BCP-47 language code (e.g., "en-US").
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
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

    # The audio_content is a byte string (MP3)
    save_audio_to_file(response.audio_content, filename)

if __name__ == '__main__':
    # Example usage:
    # Ensure you have authenticated with Google Cloud, e.g., by setting the
    # GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # For more details, refer to:
    # https://cloud.google.com/docs/authentication/getting-started

    # Create a dummy audio content for demonstration if not synthesizing
    # This part is for demonstration purposes without actual synthesis
    # In a real scenario, you would get audio_content from a TTS service response.
    dummy_audio_content = b"This is a dummy audio content."
    save_audio_to_file(dummy_audio_content, "dummy_output.mp3")

    # Example of actual synthesis and saving (requires Google Cloud setup)
    # try:
    #     synthesize_and_save_audio(
    #         text="Hello, this is a test of Google Cloud Text-to-Speech.",
    #         filename="hello_world.mp3",
    #         voice_name="en-US-Wavenet-C"
    #     )
    # except Exception as e:
    #     print(f"Could not synthesize speech. Please ensure Google Cloud authentication is set up. Error: {e}")
