import boto3

def generate_spoken_brief(search_results):
    polly_client = boto3.client('polly')
    speech_text = ' '.join(search_results)
    response = polly_client.synthesize_speech(
        Text=speech_text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('brief.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

# Example usage
search_results = ['Result 1', 'Result 2', 'Result 3']
generate_spoken_brief(search_results)