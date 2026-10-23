from safety_client import load_safety_config


def reviewer_brief_audio(payload, config=None):
    import boto3

    cfg = load_safety_config(config)
    client = boto3.client("polly", region_name=cfg["region"])
    text = (payload or {}).get("text", "")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId="Joanna", Engine="neural")
    return {"audio_stream": response.get("AudioStream").read(), "provider": "aws-polly"}
