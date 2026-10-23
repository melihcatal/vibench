import boto3


def generate_reviewer_brief_audio(brief_text: str) -> bytes:
    """
    Generates an audio file from text using Amazon Polly.
    """
    polly_client = boto3.client("polly")

    response = polly_client.synthesize_speech(
        VoiceId="Joanna", OutputFormat="mp3", Text=brief_text, Engine="neural"
    )

    return response["AudioStream"].read()
