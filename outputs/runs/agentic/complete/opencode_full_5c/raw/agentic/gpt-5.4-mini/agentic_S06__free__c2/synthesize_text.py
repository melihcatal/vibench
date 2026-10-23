from azure.cognitiveservices.speech import (
    ResultReason,
    SpeechSynthesisOutputFormat,
    AudioDataStream,
)

from speech_client import build_synthesizer
from speech_models import SpeechRequest, SpeechResponse, normalize_text


def synthesize_text(text: str, locale: str = None, voice: str = None) -> SpeechResponse:
    request = SpeechRequest(
        text=normalize_text(text),
        locale=locale,
        voice=voice,
        format="audio-16khz-64kbitrate-mono-mp3",
    )
    synthesizer = build_synthesizer(
        SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3
    )
    if request.voice:
        synthesizer.speech_config.speech_synthesis_voice_name = request.voice
    result = synthesizer.speak_text_async(request.text).get()
    if result.reason != ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(str(result.reason))
    stream = AudioDataStream(result)
    audio = stream.read_data()
    return SpeechResponse(
        audio=audio,
        content_type="audio/mpeg",
        voice=request.voice,
        metadata={"locale": request.locale},
    )
