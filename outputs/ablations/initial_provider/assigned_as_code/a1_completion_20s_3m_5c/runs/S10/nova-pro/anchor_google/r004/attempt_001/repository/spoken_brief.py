import os
import google.auth
from google.cloud import texttospeech


def generate_spoken_brief(text):
    credentials, _ = google.auth.default()
    text_to_speech_client = texttospeech.TextToSpeechClient(credentials=credentials)
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = text_to_speech_client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
    return 'output.mp3'