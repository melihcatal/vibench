import os
from google.cloud import texttospeech


def generate_reviewer_brief_audio(
    text: str, output_filepath: str = "reviewer_brief.mp3"
):
    """
    Generate spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS_PATH"
    )  # Assuming path to credentials file
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Configure the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response to the output file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)
