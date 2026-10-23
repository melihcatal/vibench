import boto3

def synthesize_text(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response['AudioStream'].read()

if __name__ == '__main__':
    text = 'Hello, this is a test of the Amazon Polly service.'
    audio_stream = synthesize_text(text)
    with open('output.mp3', 'wb') as f:
        f.write(audio_stream)