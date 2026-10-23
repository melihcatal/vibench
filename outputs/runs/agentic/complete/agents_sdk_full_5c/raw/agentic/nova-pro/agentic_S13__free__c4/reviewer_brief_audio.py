import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient(api_key=os.getenv('GOOGLE_CLOUD_TEXT_TO_SPEECH_API_KEY'))

def generate_brief_audio(text):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open('reviewer_brief.mp3', 'wb') as out:
        out.write(response.audio_content)