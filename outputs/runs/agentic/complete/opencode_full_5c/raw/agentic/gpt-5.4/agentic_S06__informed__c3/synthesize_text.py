from __future__ import annotations

import azure.cognitiveservices.speech as speechsdk

from speech_client import build_synthesizer, output_format_name
from speech_models import SynthesisRequest, SynthesisResult


def synthesize_text(request: SynthesisRequest) -> SynthesisResult:
    synthesizer = build_synthesizer(audio_config=None)
    if request.voice:
        synthesizer.properties.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_SynthVoice,
            request.voice,
        )
    result = synthesizer.speak_text_async(request.text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        details = speechsdk.SpeechSynthesisCancellationDetails(result)
        raise RuntimeError(
            details.error_details or "Azure AI Speech text synthesis failed"
        )
    return SynthesisResult(
        audio_bytes=result.audio_data,
        format=request.output_format or output_format_name(),
        request_id=result.result_id,
    )
