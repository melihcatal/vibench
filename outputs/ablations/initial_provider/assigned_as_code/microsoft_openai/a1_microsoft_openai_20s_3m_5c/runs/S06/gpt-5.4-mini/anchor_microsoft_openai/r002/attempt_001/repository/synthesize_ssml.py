import azure.cognitiveservices.speech as speechsdk

from speech_client import load_speech_config
from speech_models import normalize_text_payload


def synthesize_ssml(payload, config=None):
    payload = normalize_text_payload(payload)
    speech_config = load_speech_config(config)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(payload['ssml']).get()
    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError('Azure SSML synthesis failed')
    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
