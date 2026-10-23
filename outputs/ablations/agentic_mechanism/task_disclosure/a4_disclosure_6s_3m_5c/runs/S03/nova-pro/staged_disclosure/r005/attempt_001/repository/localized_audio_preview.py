import boto3

def generate_audio(text, output_format='mp3', voice='Joanna'):
    polly = boto3.client('polly')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice
    )
    with open('audio_preview.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

if __name__ == '__main__':
    sample_text = 'This is a sample text to be converted into speech.'
    generate_audio(sample_text)