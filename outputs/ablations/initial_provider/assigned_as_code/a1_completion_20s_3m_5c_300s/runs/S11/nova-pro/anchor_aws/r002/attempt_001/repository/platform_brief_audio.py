import boto3


def generate_spoken_briefing(text):
    client = boto3.client("polly")
    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna",
    )
    audio_stream = response["AudioStream"]
    return audio_stream