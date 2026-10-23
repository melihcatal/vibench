
import os
from google.cloud import texttospeech

def generate_audio_briefing(text, output_filename="briefing.mp3"):
    """Generates an audio briefing from the given text using Google Cloud Text-to-Speech."""

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of voice to use
    # You can explore available voices here: https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-C",  # A high-quality voice
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
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # or ensure your environment is authenticated with gcloud

    briefing_text = "This is a brief audio summary of the platform's recent activities. All systems are operating normally, and no anomalies were detected."
    generate_audio_briefing(briefing_text, "platform_briefing.mp3")
