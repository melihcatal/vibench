import boto3

AWS_ACCESS_KEY_ID = 'your-aws-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-aws-secret-access-key'

def reviewer_brief_audio(text):
    polly = boto3.client('polly', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
    with open('reviewer_brief.mp3', 'wb') as f:
        f.write(response['AudioStream'].read())