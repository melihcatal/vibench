from google.cloud import texttospeech

def synthesize_speech(text, output_file):
    config = texttospeech.SynthesisInput(text=text)
    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(config, texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL), texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
    with open(output_file, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {output_file}')

if __name__ == '__main__':
    synthesize_speech('Hello, world!', 'output.mp3')