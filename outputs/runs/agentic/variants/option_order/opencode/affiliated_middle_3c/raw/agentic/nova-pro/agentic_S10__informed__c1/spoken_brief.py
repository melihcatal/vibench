import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()


def synthesize_speech(input_text, output_file):
    input_text = texttospeech.SynthesisInput(text=input_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print("Audio content written to file: ", output_file)
