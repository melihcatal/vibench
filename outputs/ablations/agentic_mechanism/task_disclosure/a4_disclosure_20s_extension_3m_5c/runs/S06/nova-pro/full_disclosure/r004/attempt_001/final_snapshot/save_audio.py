import boto3


def save_audio(text, output_file):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    if 'AudioStream' in response:
        with open(output_file, 'wb') as file:
            file.write(response['AudioStream'].read())
    else:
        raise ValueError('AudioStream not found in response')


if __name__ == '__main__':
    text_to_speak = 'Hello, this is a test audio file.'
    save_audio(text_to_speak, 'output.mp3')