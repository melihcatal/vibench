import boto3

polly_client = boto3.client('polly')

def generate_audio(text):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('briefing.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Audio file created successfully.')

# Example usage
generate_audio('This is a test briefing.')