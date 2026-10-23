import boto3


def generate_spoken_preview(text: str, aws_region: str | None = None) -> bytes:
    polly = boto3.client("polly", region_name=aws_region)
    result = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna", Engine="neural")
    return result["AudioStream"].read()
