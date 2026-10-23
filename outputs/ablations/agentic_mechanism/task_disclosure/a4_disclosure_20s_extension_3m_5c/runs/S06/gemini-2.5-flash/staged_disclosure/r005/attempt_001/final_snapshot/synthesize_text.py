
from google.cloud import texttospeech
import os

def synthesize_text(text, output_filename="output.mp3"):
    """Synthesizes plain text to an audio byte stream using Google Cloud Text-to-Speech."""

    # Set up Google Cloud credentials (replace with your actual credential setup)
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/credentials.json"

    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-C",  # Example Wavenet voice
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable before running
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    
    # Check if the environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable to your service account key file path.")
        print("Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"")
    else:
        synthesize_text("Hello, this is a test of Google Cloud Text-to-Speech.", "hello.mp3")
