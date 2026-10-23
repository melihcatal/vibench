import boto3
from model_models import AudioResult


def generate_audio_briefing(text_to_speak: str, output_file_path: str) -> AudioResult:
    """
    Generates a spoken audio briefing from text using Amazon Polly.
    """
    polly_client = boto3.client("polly")

    response = polly_client.synthesize_speech(
        Text=text_to_speak, OutputFormat="mp3", VoiceId="Joanna"
    )

    with open(output_file_path, "wb") as f:
        f.write(response["AudioStream"].read())

    return AudioResult(
        output_path=output_file_path,
        raw_result={
            "ContentType": response["ContentType"],
            "RequestCharacters": response["RequestCharacters"],
        },
    )
