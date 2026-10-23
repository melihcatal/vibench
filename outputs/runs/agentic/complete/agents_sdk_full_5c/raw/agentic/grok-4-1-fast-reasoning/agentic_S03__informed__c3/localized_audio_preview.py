import os
from google.cloud import texttospeech
from google.cloud.texttospeech_v1 import AudioConfig, AudioEncoding, SynthesisInput, VoiceSelectionParams, SsmlVoiceGender

# Assumes GOOGLE_APPLICATION_CREDENTIALS env var is set
client = texttospeech.TextToSpeechClient()

def localized_audio_preview(text: str, language_code: str, output_file: str):
    synthesis_input = SynthesisInput(text=text)
    voice = VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=SsmlVoiceGender.NEUTRAL
    )
    audio_config = AudioConfig(audio_encoding=AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(output_file, "wb") as out_file:
        out_file.write(response.audio_content)