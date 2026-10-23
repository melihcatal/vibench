import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config, synthesize_with_sdk
from speech_models import normalize_ssml_payload, audio_response


def synthesize_ssml(payload, config=None):
    config = config or {}
    payload = normalize_ssml_payload(payload)
    speech_config = load_speech_config(config)
    result = synthesize_with_sdk(
        speech_config,
        ssml=payload['ssml'],
        output_format=speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3,
    )
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError('Azure speech synthesis failed')
    return audio_response(result.audio_data)
