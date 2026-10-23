import os
from google.cloud import texttospeech

def save_audio_to_file(text, output_filename="output.mp3"):
    """
    Synthesizes speech from the input text and saves it to a local audio file.
    Uses Google Cloud Text-to-Speech.
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
    # Example usage:
    # Ensure you have authenticated with Google Cloud, e.g., using `gcloud auth application-default login`
    # or by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    input_text = "Hello, this is a test of the Google Cloud Text-to-Speech API."
    save_audio_to_file(input_text)
