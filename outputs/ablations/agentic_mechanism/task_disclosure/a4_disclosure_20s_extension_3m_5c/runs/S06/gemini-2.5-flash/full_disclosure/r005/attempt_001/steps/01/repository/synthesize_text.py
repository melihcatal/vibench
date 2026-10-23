from google.cloud import texttospeech

def synthesize_text(text: str, output_filename: str = "output.mp3"):
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        output_filename: The name of the file to save the audio to. Defaults to "output.mp3".
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice gender (optional)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
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
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or authenticate your gcloud CLI
    # For more info: https://cloud.google.com/docs/authentication/getting-started
    synthesize_text("Hello, this is a test of the Google Cloud Text-to-Speech API.", "hello_world.mp3")
