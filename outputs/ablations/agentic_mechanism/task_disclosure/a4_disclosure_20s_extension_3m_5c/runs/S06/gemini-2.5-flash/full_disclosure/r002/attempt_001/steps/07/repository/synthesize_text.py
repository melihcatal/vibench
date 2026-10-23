from google.cloud import texttospeech
import os

def synthesize_text(text: str, output_filename: str = "output.mp3"):
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        output_filename: The name of the file to save the audio to.
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

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
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise. For example:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"

    # Example usage
    text_to_synthesize = "Hello, this is a test of Google Cloud Text-to-Speech."
    synthesize_text(text_to_synthesize)
