import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"

polly = boto3.client(
    "polly",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-west-2",
)


def platform_brief_audio(text):
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    return response
