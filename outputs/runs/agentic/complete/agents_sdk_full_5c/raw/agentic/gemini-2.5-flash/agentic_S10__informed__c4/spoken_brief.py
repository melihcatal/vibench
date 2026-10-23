import os
from google.cloud import texttospeech
import logging

def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3"):
    """
    Generates a spoken brief from the model output using Google Cloud Text-to-Speech.
    
    Args:
        text: The text to convert to speech.
        output_filepath: The path to save the generated audio file.
    """
    # Initialize the client. Google Cloud Text-to-Speech automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # or other default credentials if set up.
    client = texttospeech.TextToSpeechClient()

    # Set the text input
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice parameters
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",  # You can choose different voices, e.g., "en-US-Wavenet-A"
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Configure the audio output format
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    try:
        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Write the audio content to a file
        with open(output_filepath, "wb") as out:
            out.write(response.audio_content)
        print(f"Audio content written to file '{output_filepath}'")
    except Exception as e:
        logging.error(f"Error generating spoken brief: {e}")
        print(f"Error: {e}")

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or your Google Cloud SDK is configured for authentication.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    model_output_text = "This is a brief summary of the generated model output. It provides a concise overview of the key findings."
    generate_spoken_brief(model_output_text, "model_brief.mp3")

    another_output = "The cat sat on the mat. This is a simple sentence for speech synthesis."
    generate_spoken_brief(another_output, "simple_sentence.mp3")
