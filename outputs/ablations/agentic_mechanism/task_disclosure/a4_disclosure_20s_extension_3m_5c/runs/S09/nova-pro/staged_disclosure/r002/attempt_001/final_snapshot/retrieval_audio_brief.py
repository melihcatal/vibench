import boto3

def generate_speech(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('speech.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

if __name__ == '__main__':
    search_results = 'Sample search results text.'
    generate_speech(search_results)