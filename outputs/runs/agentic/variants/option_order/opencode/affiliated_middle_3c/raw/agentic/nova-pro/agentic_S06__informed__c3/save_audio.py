import boto3

polly_client = boto3.client(
    "polly",
    aws_access_key_id="YOUR_AWS_ACCESS_KEY_ID",
    aws_secret_access_key="YOUR_AWS_SECRET_ACCESS_KEY",
    region_name="us-west-2",
)


def save_audio(audio_stream, file_path):
    with open(file_path, "wb") as file:
        file.write(audio_stream)
