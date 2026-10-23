import boto3


def generate_localized_audio_preview(text):
    polly = boto3.client("polly")
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    with open("audio.mp3", "wb") as f:
        f.write(response["AudioStream"].read())
