import boto3


def localized_audio_preview(text, target_lang):
    client = boto3.client("polly")
    response = client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna", LanguageCode=target_lang
    )
    with open("speech.mp3", "wb") as f:
        f.write(response["AudioStream"].read())
