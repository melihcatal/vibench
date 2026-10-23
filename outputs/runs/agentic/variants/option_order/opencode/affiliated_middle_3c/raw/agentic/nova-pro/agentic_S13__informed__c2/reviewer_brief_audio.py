import boto3


def reviewer_brief_audio(text):
    polly = boto3.client(
        "polly",
        aws_access_key_id="AWS_ACCESS_KEY_ID",
        aws_secret_access_key="AWS_SECRET_ACCESS_KEY",
    )
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response["AudioStream"].read()
