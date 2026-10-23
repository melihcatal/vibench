from __future__ import annotations

import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config
from speech_models import TTSRequest, TTSResponse, normalize_text


def synthesize_text(request: TTSRequest) -> TTSResponse:
    config = get_speech_config()
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=None)
    text = normalize_text(request.text)
    result = synthesizer.speak_text_async(text).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure Speech synthesis failed: {result.reason}")
    return TTSResponse(audio=bytes(result.audio_data), content_type="audio/mpeg", voice_name=request.voice_name, locale=request.locale)
