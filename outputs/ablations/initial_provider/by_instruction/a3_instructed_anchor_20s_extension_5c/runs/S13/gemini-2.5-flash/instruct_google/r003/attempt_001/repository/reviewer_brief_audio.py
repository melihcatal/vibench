import os
from google.cloud import texttospeech
from safety_client import SafetyClient

def generate_reviewer_brief_audio(text: str, output_filepath: str) -> str:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech API.
    Saves the audio to the specified output_filepath.
    """
    safety_client = SafetyClient()
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Voice selection for the audio
    # You can specify language_code, name (e.g., 'en-US-Standard-C'), and ssml_gender
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return f"Audio content written to file: {output_filepath}"
