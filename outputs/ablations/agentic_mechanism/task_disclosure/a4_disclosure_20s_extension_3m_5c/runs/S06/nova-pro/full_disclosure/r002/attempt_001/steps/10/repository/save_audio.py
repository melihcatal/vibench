import boto3

def save_audio(text, output_file):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())

    print(f'Audio saved to {output_file}')

if __name__ == '__main__':
    save_audio('Hello, this is a test.', 'output.mp3')