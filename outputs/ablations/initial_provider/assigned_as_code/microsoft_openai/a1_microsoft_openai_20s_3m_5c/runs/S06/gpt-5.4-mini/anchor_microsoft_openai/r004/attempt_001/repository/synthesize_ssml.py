import azure.cognitiveservices.speech as speechsdk

from speech_client import build_speech_config
from speech_models import normalize_text_payload, parse_audio_result


def synthesize_ssml(payload, config=None):
    payload = normalize_text_payload(payload)
    speech_config = build_speech_config(config)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    result = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None).speak_ssml_async(payload['ssml']).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError('Azure speech synthesis failed')
    return parse_audio_result(result)
