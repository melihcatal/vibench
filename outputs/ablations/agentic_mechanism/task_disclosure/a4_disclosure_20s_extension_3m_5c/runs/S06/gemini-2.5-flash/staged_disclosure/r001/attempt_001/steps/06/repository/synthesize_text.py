from google.cloud import texttospeech
import os

def synthesize_text(text, output_filename="output.mp3"):
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech."""

    # Set up Google Cloud credentials (if not already set via environment variable)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/keyfile.json"

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice gender
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    text_to_synthesize = "Hello, this is a test of the Google Cloud Text-to-Speech API."
    synthesize_text(text_to_synthesize)
