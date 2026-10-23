import boto3


def generate_audio_preview(text, voice_id='Joanna'):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural'
    )
    with open('audio_preview.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Audio preview saved as audio_preview.mp3')


if __name__ == '__main__':
    translated_text = 'This is a sample translated text.'
    generate_audio_preview(translated_text)