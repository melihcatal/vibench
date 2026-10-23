import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

def generate_audio_brief(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open('audio.mp3', 'wb') as out:
        out.write(response.audio_content)
    return 'audio.mp3'