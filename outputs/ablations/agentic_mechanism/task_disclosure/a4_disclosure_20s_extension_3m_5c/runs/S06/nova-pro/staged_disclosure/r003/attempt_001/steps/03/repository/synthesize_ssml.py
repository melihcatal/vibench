import boto3

def synthesize_ssml(ssml_text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=ssml_text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        TextType='ssml'
    )
    with open('output.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())
        
    print('SSML synthesized successfully.')

if __name__ == '__main__':
    ssml_text = '<speak>Hello, world!</speak>'
    synthesize_ssml(ssml_text)