from __future__ import annotations

import azure.cognitiveservices.speech as speechsdk

from speech_client import get_speech_config
from speech_models import TTSRequest, TTSResponse, normalize_ssml


def synthesize_ssml(request: TTSRequest) -> TTSResponse:
    config = get_speech_config()
    if request.voice_name:
        config.speech_synthesis_voice_name = request.voice_name
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=None)
    ssml = normalize_ssml(request.text)
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure Speech SSML synthesis failed: {result.reason}")
    return TTSResponse(audio=bytes(result.audio_data), content_type="audio/mpeg", voice_name=request.voice_name, locale=request.locale, metadata={"speaking_rate": request.speaking_rate, "pitch": request.pitch})
