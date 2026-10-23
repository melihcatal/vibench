from google.cloud import texttospeech

def get_client():
    return texttospeech.TextToSpeechClient()

def synthesize_speech(text, voice, output_file):
    client = get_client()
    input_text = texttospeech.SynthesisInput(text=text)
    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=voice['language_code'],
        ssml_gender=texttospeech.SsmlVoiceGender[voice['gender']]
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text,
        voice=voice_selection_params,
        audio_config=audio_config
    )
    with open(output_file, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {output_file}')

if __name__ == '__main__':\n    synthesize_speech('Hello, world!', {'language_code': 'en-US', 'gender': 'FEMALE'}, 'output.mp3')