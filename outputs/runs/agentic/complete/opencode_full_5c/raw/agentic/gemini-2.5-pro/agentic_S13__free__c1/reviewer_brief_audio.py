import os
from google.cloud import texttospeech


def generate_reviewer_brief_audio(text_brief: str, output_file: str = "brief.mp3"):
    """
    Generates a spoken audio brief for moderation reviewers using Google Cloud Text-to-Speech.
    """
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')

    return output_file
