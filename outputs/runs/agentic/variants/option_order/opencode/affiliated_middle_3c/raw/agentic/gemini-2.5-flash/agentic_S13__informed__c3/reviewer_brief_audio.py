import os
from google.cloud import texttospeech


def generate_reviewer_brief_audio(
    text: str, output_filename: str = "reviewer_brief.mp3"
) -> str:
    client = texttospeech.TextToSpeechClient()
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

    return output_filename
