import os
from google.cloud import texttospeech


def reviewer_brief_audio(text_brief: str, output_filepath: str = "reviewer_brief.mp3"):
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or explicit credentials provided.
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text_brief)

    # Configure the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the audio content to a file
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
