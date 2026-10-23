from google.cloud import texttospeech

def get_client():
    return texttospeech.TextToSpeechClient()

def synthesize_text(text, voice, output_file):
    input_text = texttospeech.SynthesizeInput(text=text)
    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=voice['language_code'],
        ssml_gender=voice['ssml_gender']
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    synthesis_input = texttospeech.SynthesizeInput(text=text)
    response = get_client().synthesize_speech(
        input=synthesis_input,
        voice=voice_selection_params,
        audio_config=audio_config
    )
    with open(output_file, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {output_file}')

if __name__ == '__main__':
    synthesize_text('Hello, world!', {'language_code': 'en-US', 'ssml_gender': texttospeech.SsmlVoiceGender.NEUTRAL}, 'output.mp3')