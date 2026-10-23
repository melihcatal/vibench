import boto3

polly_client = boto3.client("polly")


def generate_audio_preview(translated_text):
    response = polly_client.synthesize_speech(
        Text=translated_text, OutputFormat="mp3", VoiceId="Joanna"
    )
    return response["AudioStream"].read()
