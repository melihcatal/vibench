from safety_client import get_polly_client


def reviewer_brief_audio(payload, config=None):
    client = get_polly_client(config)
    text = (payload or {}).get("text", "")
    response = client.synthesize_speech(Text=text, OutputFormat="mp3", VoiceId=(payload or {}).get("voice", "Joanna"), Engine="neural")
    return {"audio": response.get("AudioStream"), "voice": (payload or {}).get("voice", "Joanna")}
