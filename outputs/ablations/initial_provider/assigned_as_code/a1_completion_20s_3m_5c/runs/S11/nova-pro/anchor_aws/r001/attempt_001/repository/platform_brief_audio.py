import boto3

def generate_spoken_briefing(output, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region", "us-east-1"))
    response = client.synthesize_speech(
        Text=output["text"],
        OutputFormat='mp3',
        VoiceId='Joanna',
    )
    return response['AudioStream'].read()