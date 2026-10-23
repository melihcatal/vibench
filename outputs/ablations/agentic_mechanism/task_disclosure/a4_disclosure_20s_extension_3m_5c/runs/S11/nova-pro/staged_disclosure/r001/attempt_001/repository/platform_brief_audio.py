import boto3

def generate_briefing(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('briefing.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Briefing generated as briefing.mp3')

# Example usage
generate_briefing('This is a test briefing.')