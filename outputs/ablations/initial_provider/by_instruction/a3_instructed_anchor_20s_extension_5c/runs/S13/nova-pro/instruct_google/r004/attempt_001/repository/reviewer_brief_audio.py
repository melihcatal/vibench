import os
from google.cloud import texttospeech

def generate_reviewer_brief_audio(text):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open('reviewer_brief.mp3', 'wb') as out:
        out.write(response.audio_content)
    print('Audio file generated: reviewer_brief.mp3')

if __name__ == '__main__':
    sample_text = 'This is a reviewer brief to generate audio for.'
    generate_reviewer_brief_audio(sample_text)
