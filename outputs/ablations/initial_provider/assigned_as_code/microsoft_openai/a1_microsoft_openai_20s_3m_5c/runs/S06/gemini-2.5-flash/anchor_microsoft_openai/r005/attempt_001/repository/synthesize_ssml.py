import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import SynthesisPayload


def synthesize_ssml(payload: SynthesisPayload):
    speech_config = get_speech_config()
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    if payload.voice_name:
        speech_config.speech_synthesis_voice_name = payload.voice_name

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(payload.ssml).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure SSML synthesis failed: {result.cancellation_details.reason}")

    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
