
import os
from google.cloud import texttospeech

def save_audio(text: str, output_filepath: str):
    """
    Synthesizes speech from the input text and writes it to a local audio file.

    Args:
        text (str): The text to synthesize.
        output_filepath (str): The path to the file where the audio will be saved.
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

    # The audio content can be streamed from the response.
    # In this case, we write the response to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'''Audio content written to "{output_filepath}"''')

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    # save_audio("Hello, this is a test of Google Cloud Text-to-Speech.", "output.mp3")
    pass
