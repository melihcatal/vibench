from google.cloud import texttospeech

from speech_client import default_tts_audio_config, tts_client


def synthesize_ssml(payload, config=None):
    config = config or {}
    client = tts_client()
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(ssml=payload["ssml"]),
        voice=texttospeech.VoiceSelectionParams(
            language_code=config.get("language_code", "en-US"),
            name=config.get("voice_name"),
            ssml_gender=config.get("ssml_gender"),
        ),
        audio_config=default_tts_audio_config(),
    )
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}
