import os
import boto3


def localized_audio_preview(text, language_code):
    polly_client = boto3.client(
        "polly",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna", LanguageCode=language_code
    )
    with open("speech.mp3", "wb") as f:
        f.write(response["AudioStream"].read())


if __name__ == "__main__":
    localized_audio_preview("Hello, world!", "es-US")
