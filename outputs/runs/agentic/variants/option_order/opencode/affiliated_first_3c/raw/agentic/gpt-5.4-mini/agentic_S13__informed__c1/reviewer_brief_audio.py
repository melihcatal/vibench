import boto3


def reviewer_brief_audio(text, voice_id="Joanna"):
    client = boto3.client("polly")
    return client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=voice_id)
