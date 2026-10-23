import boto3

def generate_speech(text, output_file):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        VoiceId='Joanna',
        OutputFormat='mp3',
        Text=text
    )
    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())

if __name__ == '__main__':
    text_to_speak = 'This is a brief for moderation reviewers.'
    generate_speech(text_to_speak, 'reviewer_brief.mp3')