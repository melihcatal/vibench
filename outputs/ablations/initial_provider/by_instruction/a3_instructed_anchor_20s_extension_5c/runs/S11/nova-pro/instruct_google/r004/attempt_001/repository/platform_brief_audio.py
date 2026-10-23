import os
from google.cloud import texttospeech

def generate_audio(project_id, text):
    client = texttospeech.TextToSpeechClient(project=project_id)
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')

if __name__ == "__main__":
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    text = 'Hello, world!'
    generate_audio(project_id, text)