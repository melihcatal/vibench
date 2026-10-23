from speech_client import get_tts_client, build_synthesis_request, synthesize_audio
from speech_models import TTSRequest, TTSResponse, build_ssml


def synthesize_ssml(
    ssml: str = None,
    text: str = None,
    voice_name: str = "en-US-Neural2-F",
    language_code: str = "en-US",
    audio_encoding: str = "MP3",
    speaking_rate: float = 1.0,
    pitch: float = 0.0,
    volume: str = "default",
) -> TTSResponse:
    if ssml is None and text is not None:
        ssml = build_ssml(
            text=text,
            voice_name=voice_name,
            language_code=language_code,
            speaking_rate=speaking_rate,
            pitch=pitch,
            volume=volume,
        )

    request_data = TTSRequest(
        ssml=ssml,
        language_code=language_code,
        voice_name=voice_name,
        audio_encoding=audio_encoding,
        speaking_rate=speaking_rate,
        pitch=pitch,
    )
    request_data.validate()

    client = get_tts_client()
    synthesis_request = build_synthesis_request(
        ssml=request_data.ssml,
        language_code=request_data.language_code,
        voice_name=request_data.voice_name,
        audio_encoding=request_data.audio_encoding,
        speaking_rate=request_data.speaking_rate,
        pitch=request_data.pitch,
    )

    audio_content = synthesize_audio(client, synthesis_request)

    text_length = len(ssml) if ssml else 0
    return TTSResponse(
        audio_content=audio_content,
        audio_format=request_data.audio_encoding,
        voice_name=request_data.voice_name,
        language_code=request_data.language_code,
        character_count=text_length,
    )
