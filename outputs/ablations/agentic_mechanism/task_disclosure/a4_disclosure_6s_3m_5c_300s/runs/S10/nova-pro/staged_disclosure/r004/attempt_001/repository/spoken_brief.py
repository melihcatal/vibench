import boto3

def generate_spoken_brief(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('spoken_brief.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Spoken brief generated as spoken_brief.mp3')

# Example usage
generate_spoken_brief('This is a test brief.')