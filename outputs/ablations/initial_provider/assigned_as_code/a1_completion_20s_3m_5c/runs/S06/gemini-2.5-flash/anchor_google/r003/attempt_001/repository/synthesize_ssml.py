from google.cloud import texttospeech


def synthesize_ssml(payload, config=None):
    config = config or {}
    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(input=texttospeech.SynthesisInput(ssml=payload["ssml"]),
        voice=texttospeech.VoiceSelectionParams(
            language_code=config.get("language_code", "en-US"),
            name=config.get("voice_name")
        ),
        audio_config=texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=config.get("speaking_rate", 1.0),
            pitch=config.get("pitch", 0.0)
        ))
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}
