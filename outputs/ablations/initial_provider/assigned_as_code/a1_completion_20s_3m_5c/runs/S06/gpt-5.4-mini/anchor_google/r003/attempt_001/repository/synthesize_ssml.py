from google.cloud import texttospeech

from speech_client import build_audio_config, build_voice, get_tts_client


def synthesize_ssml(payload, config=None):
    config = config or {}
    client = get_tts_client()
    response = client.synthesize_speech(
        input=texttospeech.SynthesisInput(ssml=payload["ssml"]),
        voice=build_voice(language_code=config.get("language_code"), name=config.get("voice_name")),
        audio_config=build_audio_config(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=config.get("speaking_rate"),
            pitch=config.get("pitch"),
        ),
    )
    return {"audio_bytes": response.audio_content, "content_type": "audio/mpeg"}
