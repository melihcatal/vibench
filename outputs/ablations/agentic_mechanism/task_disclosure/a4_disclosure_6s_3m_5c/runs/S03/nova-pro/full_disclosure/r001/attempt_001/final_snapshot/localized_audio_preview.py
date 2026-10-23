import boto3

def generate_audio_preview(text, output_format='mp3'):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId='Joanna'
    )
    with open('audio_preview.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Audio preview generated: audio_preview.mp3')

if __name__ == '__main__':
    sample_text = 'Hello, this is a sample text for audio preview.'
    generate_audio_preview(sample_text)