import boto3

def generate_spoken_brief(model_output):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=model_output,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('spoken_brief.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

    print('Spoken brief generated successfully.')