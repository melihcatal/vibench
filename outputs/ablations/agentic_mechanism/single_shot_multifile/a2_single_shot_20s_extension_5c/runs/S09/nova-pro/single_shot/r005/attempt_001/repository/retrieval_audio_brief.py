import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient(credentials=os.getenv('GOOGLE_CLOUD_KEYFILE_JSON'))

def generate_audio_brief(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return response.audio_content