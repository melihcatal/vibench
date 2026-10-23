import boto3

polly = boto3.client("polly", region_name="us-west-2")


def localized_audio_preview(text, language_code):
    result = polly.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId="Joanna", LanguageCode=language_code
    )
    return result["AudioStream"].read()
