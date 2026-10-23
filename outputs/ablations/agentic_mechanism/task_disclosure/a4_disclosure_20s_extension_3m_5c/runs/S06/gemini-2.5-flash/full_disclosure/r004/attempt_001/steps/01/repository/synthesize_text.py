
from google.cloud import texttospeech

def synthesize_text_to_audio(text: str, output_filepath: str = "output.mp3"):
    """
    Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech.

    Args:
        text: The plain text to synthesize.
        output_filepath: The path to save the synthesized audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL),
        audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filepath}"')

if __name__ == "__main__":
    # Example usage:
    # Set up Google Cloud authentication if you haven't already:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    synthesize_text_to_audio("Hello, world! This is a test of Google Cloud Text-to-Speech.", "hello_world.mp3")
