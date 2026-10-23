import boto3

def synthesize_text(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    if 'AudioStream' in response:
        with open('output.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
    else:
        raise Exception('AudioStream not found in response')

# Example usage:
# synthesize_text('Hello, world!')