import os
from google.cloud import text_to_speech

client = text_to_speech.TextToSpeechClient()

text = 'This is a log message.'
input_text = text_to_speech.SynthesisInput(text=text)
voice = text_to_speech.VoiceSelectionParams(language_code='en-US', ssml_gender=text_to_speech.SsmlVoiceGender.NEUTRAL)
audio_config = text_to_speech.AudioConfig(audio_encoding=text_to_speech.AudioEncoding.MP3)

response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

with open('output.mp3', 'wb') as out:
    out.write(response.audio_content)