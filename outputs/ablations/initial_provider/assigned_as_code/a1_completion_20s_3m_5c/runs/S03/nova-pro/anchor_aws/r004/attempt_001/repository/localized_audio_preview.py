import boto3


def generate_localized_audio_preview(payload, config=None):
    config = config or {}
    client = boto3.client("polly", region_name=config.get("region"))
    text = payload["text"]
    language_code = payload["language_code"]
    voice_id = payload["voice_id"]
    response = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=voice_id,
        LanguageCode=language_code,
    )
    return {
        "audio_stream": response["AudioStream"],
    }