from google.cloud import texttospeech


def synthesize_text(payload, config=None):
    config = config or {}
    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(input=texttospeech.SynthesisInput(text=payload["text"]),
        voice=texttospeech.VoiceSelectionParams(language_code=config.get("language_code", "en-US")),
        audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}
