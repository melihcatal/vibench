import boto3

def synthesize_ssml(ssml_text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=ssml_text,
        TextType='ssml'
    )
    with open('speech.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
    print('Speech synthesized to speech.mp3')

if __name__ == '__main__':
    ssml_text = '<speak>Hello, world!</speak>'
    synthesize_ssml(ssml_text)