import boto3

def generate_audio_preview(text, language_code):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=get_voice_id(language_code)
    )
    with open('audio_preview.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

def get_voice_id(language_code):
    voice_ids = {
        'en': 'Joanna',
        'es': 'Miguel',
        'fr': 'Mathieu',
        'de': 'Vicki',
        'it': 'Carla',
        'ja': 'Mizuki'
    }
    return voice_ids.get(language_code, 'Joanna')

if __name__ == '__main__':\n    text = 'Hello, world!'
    language_code = 'en'
    generate_audio_preview(text, language_code)