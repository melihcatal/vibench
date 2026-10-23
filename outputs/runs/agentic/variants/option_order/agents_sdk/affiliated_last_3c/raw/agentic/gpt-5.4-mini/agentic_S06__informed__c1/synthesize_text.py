from __future__ import annotations

from speech_client import get_polly_client, normalize_engine, normalize_output_format, normalize_voice_id
from speech_models import TTSRequest, TTSResponse


def synthesize_text(text: str, voice_id: str | None = None, output_format: str | None = None, engine: str | None = None) -> TTSResponse:
    client = get_polly_client()
    request = TTSRequest(
        text=text,
        voice_id=normalize_voice_id(voice_id),
        output_format=normalize_output_format(output_format),
        engine=normalize_engine(engine),
    )
    result = client.synthesize_speech(
        Text=request.normalized_input(),
        VoiceId=request.voice_id,
        OutputFormat=request.output_format,
        Engine=request.engine,
    )
    audio = result["AudioStream"].read()
    return TTSResponse(audio_bytes=audio, content_type=f"audio/{request.output_format}", metadata={"request_id": result.get("ResponseMetadata", {}).get("RequestId")})
