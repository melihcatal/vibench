import boto3


def reviewer_brief_audio(text):
    polly = boto3.client("polly")
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna")
    with open("reviewer_brief.mp3", "wb") as file:
        file.write(response["AudioStream"].read())
