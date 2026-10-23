import speech_client
from speech_models import SpeechRequest, SpeechResponse, normalize_text


def synthesize_text(text: str, voice_id: str | None = None, output_format: str = "mp3") -> bytes:
    req = SpeechRequest(text=normalize_text(text), voice_id=voice_id or speech_client.tts_voice("en-US"), output_format=output_format)
    resp = speech_client.polly_client().synthesize_speech(Text=req.text, VoiceId=req.voice_id, OutputFormat=req.output_format, Engine=req.engine, TextType=req.text_type)
    return resp["AudioStream"].read()


def synthesize(text: str) -> SpeechResponse:
    req = SpeechRequest(text=normalize_text(text), voice_id=speech_client.tts_voice("en-US"))
    resp = speech_client.polly_client().synthesize_speech(Text=req.text, VoiceId=req.voice_id, OutputFormat=req.output_format, Engine=req.engine, TextType=req.text_type)
    return SpeechResponse(audio_stream=resp["AudioStream"], content_type=resp.get("ContentType", "audio/mpeg"), request=req)
