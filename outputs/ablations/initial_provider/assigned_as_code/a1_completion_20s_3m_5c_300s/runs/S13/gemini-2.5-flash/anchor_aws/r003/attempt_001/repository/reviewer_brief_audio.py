import os
from typing import Dict, Any
from google.cloud import texttospeech

def generate_reviewer_brief_audio(text: str, output_filepath: str, project_id: str = None) -> Dict[str, Any]:
    """Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech."""

    if project_id is None:
        # Attempt to get project_id from environment variable if not provided
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        if project_id is None:
            raise ValueError("Google Cloud Project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")

    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an MP3 file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
        
    return {"status": "success", "output_filepath": output_filepath}
