import os
from google.cloud import texttospepeech

def synthesize_ssml(text, output_filename="output.mp3"):
    """Synthesizes SSML with voice and prosody controls using Google Cloud Text-to-Speech."""

    client = texttospeech.TextToSpeechClient()

    # Set the SSML input with voice and prosody controls
    ssml_text = f"""
        <speak>
            <prosody rate="medium" pitch="medium">
                {text}
            </prosody>
        </speak>
    """

    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

    # Configure the voice (e.g., US English, WaveNet voice)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",  # Example WaveNet voice
    )

    # Select the audio file type
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response audio content to a file
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

if __name__ == "__main__":
    # Example usage:
    # Ensure you have authenticated with Google Cloud (e.g., by setting GOOGLE_APPLICATION_CREDENTIALS)
    # For more information, see: https://cloud.google.com/docs/authentication/getting-started
    
    # Simple text to demonstrate prosody control
    synthesize_ssml("Hello, this is a test with a slightly slower pace and a normal pitch.")
