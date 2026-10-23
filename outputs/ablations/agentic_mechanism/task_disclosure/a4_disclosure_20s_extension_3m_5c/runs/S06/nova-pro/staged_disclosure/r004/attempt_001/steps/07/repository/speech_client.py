import os
from google.cloud import texttospeech

# Set environment variables for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'

# Create a client instance
client = texttospeech.TextToSpeechClient()

def synthesize_speech(text, output_file):
    """Synthesizes speech from the input string of text."""
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open(output_file, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {output_file}')
