import os
from google.cloud import texttospeech

# Set up the client
def get_text_to_speech_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'
    return texttospeech.TextToSpeechClient()

# Helper function to synthesize speech
def synthesize_speech(client, text, output_file):
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    with open(output_file, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {output_file}')
