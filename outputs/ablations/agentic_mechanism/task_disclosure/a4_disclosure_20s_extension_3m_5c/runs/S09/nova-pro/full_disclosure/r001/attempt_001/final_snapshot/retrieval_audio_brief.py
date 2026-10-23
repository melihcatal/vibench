import boto3

def generate_spoken_brief(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    if 'AudioStream' in response:
        with open('spoken_brief.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
        return 'spoken_brief.mp3'
    else:
        return 'Error generating spoken brief'