import boto3

def synthesize_ssml(ssml_text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=ssml_text,
        TextType='ssml'
    )
    if 'AudioStream' in response:
        with open('speech.mp3', 'wb') as file:
            file.write(response['AudioStream'].read())
        return 'Speech synthesized to speech.mp3'
    else:
        return 'Error synthesizing speech'

if __name__ == '__main__':
    ssml_text = '<speak>Hello, world!</speak>'
    print(synthesize_ssml(ssml_text))