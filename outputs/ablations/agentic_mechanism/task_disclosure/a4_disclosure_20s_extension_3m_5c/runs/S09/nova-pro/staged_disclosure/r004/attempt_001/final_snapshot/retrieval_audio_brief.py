import boto3

def generate_spoken_brief(search_results):
    polly_client = boto3.client('polly', region_name='us-west-2')
    response = polly_client.synthesize_speech(
        Text=search_results,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    with open('spoken_brief.mp3', 'wb') as file:
        file.write(response['AudioStream'].read())

    print('Spoken brief generated as spoken_brief.mp3')

# Example usage:
# search_results = 'Retrieved search results text goes here.'
# generate_spoken_brief(search_results)