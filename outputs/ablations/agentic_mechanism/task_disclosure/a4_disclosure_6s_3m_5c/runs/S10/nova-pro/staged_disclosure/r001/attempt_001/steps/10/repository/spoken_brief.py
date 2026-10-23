import boto3

def generate_spoken_brief(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    with open('spoken_brief.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    return 'spoken_brief.mp3'