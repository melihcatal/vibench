import boto3

def save_audio(text, file_path):
    polly = boto3.client('polly')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open(file_path, 'wb') as file:
        file.write(response['AudioStream'].read())

if __name__ == '__main__':
    text = 'Hello, this is a test of the Amazon Polly service.'
    file_path = 'output.mp3'
    save_audio(text, file_path)