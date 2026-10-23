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
        print('Spoken brief generated as spoken_brief.mp3')

if __name__ == '__main__'):
    model_output = 'This is a sample text to be converted to speech.'
    generate_spoken_brief(model_output)