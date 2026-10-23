
from google.cloud import texttospeech

def save_audio(text: str, output_filepath: str):
    """Synthesizes speech from the input text and saves it to a local file.

    Args:
        text (str): The text to synthesize.
        output_filepath (str): The path to save the audio file (e.g., "output.mp3").
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    # For a list of available voices, see https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

if __name__ == "__main__":
    # Example usage:
    # Ensure you have authenticated with Google Cloud (e.g., gcloud auth application-default login)
    # And installed the client library: pip install google-cloud-texttospeech
    save_audio("Hello, world! This is a test of Google Cloud Text-to-Speech.", "output.mp3")
