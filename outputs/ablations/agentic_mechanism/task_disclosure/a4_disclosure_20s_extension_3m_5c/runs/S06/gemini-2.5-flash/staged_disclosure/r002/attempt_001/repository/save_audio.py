from google.cloud import texttospeech
import os

def synthesize_and_save_audio(text, output_filename="output.mp3"):
    """Synthesizes speech from the input text and saves it to a local file.

    Args:
        text (str): The text to synthesize.
        output_filename (str): The name of the file to save the audio to.
    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",  # This is a Google Cloud-specific voice identifier
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    # The audio content is binary.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise for Google Cloud.
    # For local development, you might need to run:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    
    # Check if the environment variable is set
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
        print("Please set it to the path of your Google Cloud service account key file.")
        print("Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"")
        print("Proceeding with example, but synthesis might fail without proper authentication.")

    synthesize_and_save_audio("Hello, this is a test of Google Cloud Text-to-Speech.", "welcome.mp3")
