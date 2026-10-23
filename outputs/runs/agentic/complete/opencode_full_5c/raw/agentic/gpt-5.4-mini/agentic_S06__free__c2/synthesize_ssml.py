from azure.cognitiveservices.speech import (
    ResultReason,
    SpeechSynthesisOutputFormat,
    AudioDataStream,
)

from speech_client import build_synthesizer
from speech_models import SpeechRequest, SpeechResponse, normalize_ssml


def synthesize_ssml(
    ssml: str,
    voice: str,
    locale: str = None,
    prosody_rate: str = None,
    prosody_pitch: str = None,
) -> SpeechResponse:
    request = SpeechRequest(
        text=normalize_ssml(ssml),
        locale=locale,
        voice=voice,
        format="audio-16khz-64kbitrate-mono-mp3",
    )
    synthesizer = build_synthesizer(
        SpeechSynthesisOutputFormat.Audio16Khz64KBitRateMonoMp3
    )
    synthesized = request.text
    if voice:
        synthesized = synthesized.replace("<voice>", f'<voice name="{voice}">')
    if prosody_rate or prosody_pitch:
        synthesized = synthesized.replace(
            "<prosody>",
            f'<prosody rate="{prosody_rate or "default"}" pitch="{prosody_pitch or "default"}">',
        )
    result = synthesizer.speak_ssml_async(synthesized).get()
    if result.reason != ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(str(result.reason))
    stream = AudioDataStream(result)
    return SpeechResponse(
        audio=stream.read_data(),
        content_type="audio/mpeg",
        voice=voice,
        metadata={"locale": locale},
    )
