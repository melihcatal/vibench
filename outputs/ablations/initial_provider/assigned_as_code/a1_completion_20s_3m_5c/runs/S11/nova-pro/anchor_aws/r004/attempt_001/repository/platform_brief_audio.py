import boto3


def generate_brief_audio(output, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    response = client.synthesize_speech(
        Text=output,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response['AudioStream'].read()