import os
from google.cloud import texttospeech_v1 as tts_v1

def reviewer_brief_audio(text):
    client = tts_v1.TextToSpeechClient()
    input_text = tts_v1.SynthesisInput(text=text)
    voice = tts_v1.VoiceSelectionParams(language_code='en-US', ssml_gender=tts_v1.SsmlVoiceGender.NEUTRAL)
    audio_config = tts_v1.AudioConfig(audio_encoding=tts_v1.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
    return 'output.mp3'
