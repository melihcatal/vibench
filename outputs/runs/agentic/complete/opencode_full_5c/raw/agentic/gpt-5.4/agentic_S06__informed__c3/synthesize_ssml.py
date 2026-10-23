from __future__ import annotations

from xml.sax.saxutils import escape

import azure.cognitiveservices.speech as speechsdk

from speech_client import build_synthesizer, output_format_name
from speech_models import SynthesisRequest, SynthesisResult, normalize_locale


def _build_ssml(request: SynthesisRequest) -> str:
    locale = normalize_locale(request.locale) or "en-US"
    voice = request.voice or "en-US-JennyNeural"
    rate = request.rate or "0%"
    pitch = request.pitch or "0%"
    text = escape(request.text)
    style_open = (
        f'<mstts:express-as style="{escape(request.style)}">' if request.style else ""
    )
    style_close = "</mstts:express-as>" if request.style else ""
    return (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{locale}">'
        f'<voice name="{voice}"><prosody rate="{rate}" pitch="{pitch}">{style_open}{text}{style_close}'
        f"</prosody></voice></speak>"
    )


def synthesize_ssml(request: SynthesisRequest) -> SynthesisResult:
    synthesizer = build_synthesizer(audio_config=None)
    result = synthesizer.speak_ssml_async(_build_ssml(request)).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        details = speechsdk.SpeechSynthesisCancellationDetails(result)
        raise RuntimeError(
            details.error_details or "Azure AI Speech SSML synthesis failed"
        )
    return SynthesisResult(
        audio_bytes=result.audio_data,
        format=request.output_format or output_format_name(),
        request_id=result.result_id,
    )
