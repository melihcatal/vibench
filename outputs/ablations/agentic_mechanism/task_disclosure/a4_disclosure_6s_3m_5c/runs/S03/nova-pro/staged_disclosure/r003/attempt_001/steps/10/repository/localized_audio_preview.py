import boto3

def generate_audio(text, language_code):
    polly_client = boto3.client('polly', region_name='us-west-2')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna',
        LanguageCode=language_code
    )
    with open('audio.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

    print('Audio saved as audio.mp3')

# Example usage
generate_audio('Hello, world!', 'en-US')