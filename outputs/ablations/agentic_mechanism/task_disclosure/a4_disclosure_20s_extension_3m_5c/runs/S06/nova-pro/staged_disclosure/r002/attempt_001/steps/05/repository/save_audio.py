import boto3

def save_audio(text, file_name):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    with open(file_name, 'wb') as file:
        file.write(response['AudioStream'].read())

if __name__ == '__main__':
    save_audio('Hello, this is a test.', 'output.mp3')