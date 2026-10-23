from speech_client import build_polly_client
from speech_models import TextToSpeechRequest, TextToSpeechResponse, normalize_text


def synthesize_text(text: str, voice_id: str = "Joanna", output_format: str = "mp3") -> TextToSpeechResponse:
    client = build_polly_client()
    request = TextToSpeechRequest(text=normalize_text(text), voice_id=voice_id, output_format=output_format)
    result = client.synthesize_speech(
        Text=request.text,
        VoiceId=request.voice_id,
        OutputFormat=request.output_format,
        Engine=request.engine,
        SampleRate=request.sample_rate,
    )
    return TextToSpeechResponse(
        audio_bytes=result["AudioStream"].read(),
        content_type=result.get("ContentType", "audio/mpeg"),
        request_meta={"voice_id": request.voice_id, "output_format": request.output_format, "engine": request.engine},
    )
