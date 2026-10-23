from azure.cognitiveservices import speech as speechsdk

from speech_client import create_synthesizer, load_speech_config, normalize_voice_name
from speech_models import SSMLRequest, TTSResponse, make_ssml


def synthesize_ssml(ssml: str, locale: str = "en-US", voice: str = None, rate: str = "0%", pitch: str = "0%") -> TTSResponse:
    cfg = load_speech_config()
    selected_voice = normalize_voice_name(locale, voice or cfg.voice) or "en-US-JennyNeural"
    request = SSMLRequest(ssml=ssml, locale=locale, voice=selected_voice)
    synthesizer = create_synthesizer()
    synthesizer.speech_synthesis_voice_name = request.voice
    payload = request.ssml if request.ssml.strip().startswith("<speak") else make_ssml(request.ssml, request.voice, rate=rate, pitch=pitch)
    result = synthesizer.speak_ssml_async(payload).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure Speech SSML synthesis failed: {result.reason}")
    return TTSResponse(audio_bytes=result.audio_data, content_type="audio/wav", voice=request.voice)
