import os
from google.cloud import texttospeech

def reviewer_brief_audio(brief_text: str, output_filepath: str = "reviewer_brief.mp3") -> str:
    """
    Generates spoken briefs for moderation reviewers using Google Cloud Text-to-Speech.
    The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice,
            "audio_config": audio_config
        }
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
