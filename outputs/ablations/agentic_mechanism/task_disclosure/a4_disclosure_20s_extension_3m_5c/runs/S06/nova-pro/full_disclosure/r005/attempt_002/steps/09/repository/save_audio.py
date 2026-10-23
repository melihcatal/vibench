import boto3

def save_audio(text, output_file):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    if 'AudioStream' in response:
        with open(output_file, 'wb') as file:
            file.write(response['AudioStream'].read())
    else:
        raise Exception('AudioStream not found in response')