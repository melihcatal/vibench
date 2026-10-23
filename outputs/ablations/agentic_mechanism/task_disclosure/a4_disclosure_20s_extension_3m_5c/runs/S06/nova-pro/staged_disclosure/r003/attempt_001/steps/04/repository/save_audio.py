import boto3

def save_audio(text, filename):
    polly = boto3.client('polly')
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    with open(filename, 'wb') as file:
        file.write(response['AudioStream'].read())

if __name__ == '__main__':
    save_audio('Hello, this is a test.', 'output.mp3')