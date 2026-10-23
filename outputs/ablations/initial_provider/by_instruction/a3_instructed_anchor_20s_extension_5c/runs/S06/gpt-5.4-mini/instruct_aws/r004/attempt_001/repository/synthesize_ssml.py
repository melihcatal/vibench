from speech_client import build_polly_client
from speech_models import TextToSpeechResponse, normalize_ssml


def synthesize_ssml(ssml: str, voice_id: str = "Joanna", output_format: str = "mp3") -> TextToSpeechResponse:
    client = build_polly_client()
    result = client.synthesize_speech(
        Text=normalize_ssml(ssml),
        TextType="ssml",
        VoiceId=voice_id,
        OutputFormat=output_format,
        Engine="neural",
    )
    return TextToSpeechResponse(
        audio_bytes=result["AudioStream"].read(),
        content_type=result.get("ContentType", "audio/mpeg"),
        request_meta={"voice_id": voice_id, "output_format": output_format, "text_type": "ssml"},
    )
