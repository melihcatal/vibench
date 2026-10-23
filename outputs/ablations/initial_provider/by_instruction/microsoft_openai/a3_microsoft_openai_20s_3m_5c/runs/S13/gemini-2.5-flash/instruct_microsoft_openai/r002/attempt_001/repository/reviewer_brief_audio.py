import os
from google.cloud import texttospeech

def generate_reviewer_brief_audio(text: str, output_filepath: str) -> None:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    
    Args:
        text (str): The text content of the brief to be converted to speech.
        output_filepath (str): The local path where the generated audio file (MP3) will be saved.
    """
    # Google Cloud Text-to-Speech automatically uses credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS) or the active gcloud configuration.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice.
    # Using a standard voice and language for demonstration.
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", 
        name="en-US-Standard-C",  # A standard male voice
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )

    # Configure the audio format.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    print(f"Audio content written to file {output_filepath}")
