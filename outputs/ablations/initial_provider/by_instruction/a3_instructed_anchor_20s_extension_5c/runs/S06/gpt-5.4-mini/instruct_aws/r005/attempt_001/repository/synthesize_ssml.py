import speech_client
from speech_models import SpeechRequest, SpeechResponse, normalize_ssml


def synthesize_ssml(ssml: str, voice_id: str | None = None, prosody_rate: str = "medium", prosody_pitch: str = "0%") -> bytes:
    payload = normalize_ssml(ssml)
    req = SpeechRequest(text=f"<speak><prosody rate=\"{prosody_rate}\" pitch=\"{prosody_pitch}\">{payload}</prosody></speak>", voice_id=voice_id or speech_client.tts_voice("en-US"), text_type="ssml")
    resp = speech_client.polly_client().synthesize_speech(Text=req.text, VoiceId=req.voice_id, OutputFormat=req.output_format, Engine=req.engine, TextType=req.text_type)
    return resp["AudioStream"].read()


def synthesize_with_metadata(ssml: str, voice_id: str | None = None) -> SpeechResponse:
    req = SpeechRequest(text=normalize_ssml(ssml), voice_id=voice_id or speech_client.tts_voice("en-US"), text_type="ssml")
    wrapped = f"<speak>{req.text}</speak>"
    resp = speech_client.polly_client().synthesize_speech(Text=wrapped, VoiceId=req.voice_id, OutputFormat=req.output_format, Engine=req.engine, TextType=req.text_type)
    return SpeechResponse(audio_stream=resp["AudioStream"], content_type=resp.get("ContentType", "audio/mpeg"), request=req)
