import boto3

from model_client import get_region


def platform_brief_audio(payload, config=None):
    config = config or {}
    polly = boto3.client("polly", region_name=get_region(config))
    response = polly.synthesize_speech(
        Text=payload["text"],
        OutputFormat=config.get("output_format", "mp3"),
        VoiceId=config.get("voice_id", "Joanna"),
        Engine=config.get("engine", "neural"),
    )
    return {"audio_stream": response["AudioStream"], "content_type": response.get("ContentType"), "response": response}
