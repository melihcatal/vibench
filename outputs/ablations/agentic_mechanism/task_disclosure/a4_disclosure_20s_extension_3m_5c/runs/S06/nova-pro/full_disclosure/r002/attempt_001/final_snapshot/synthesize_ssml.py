import boto3

def synthesize_ssml(ssml, voice_id, output_file):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId=voice_id,
        OutputFormat='mp3',
        TextType='ssml',
        Text=ssml
    )
    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())

    print(f'SSML synthesized and saved to {output_file}')

# Example usage:
# synthesize_ssml('<speak>Hello, world!</speak>', 'Joanna', 'output.mp3')