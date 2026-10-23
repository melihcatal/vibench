from speech_client import get_polly_client
from speech_models import SpeechRequest, SpeechResponse, normalize_ssml


def synthesize_ssml(ssml: str, voice_id: str = "Joanna", output_format: str = "mp3") -> SpeechResponse:
    client = get_polly_client()
    request = SpeechRequest(text=normalize_ssml(ssml), voice_id=voice_id, output_format=output_format, text_type="ssml")
    response = client.synthesize_speech(Text=request.text, TextType=request.text_type, OutputFormat=request.output_format, VoiceId=request.voice_id, Engine=request.engine)
    return SpeechResponse(audio=response["AudioStream"].read(), content_type=response.get("ContentType", "application/octet-stream"), voice_id=request.voice_id, meta={"engine": request.engine, "text_type": request.text_type})
