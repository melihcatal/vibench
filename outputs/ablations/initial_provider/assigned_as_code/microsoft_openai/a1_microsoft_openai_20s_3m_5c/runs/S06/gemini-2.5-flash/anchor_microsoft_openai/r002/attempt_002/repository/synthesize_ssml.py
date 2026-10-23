import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import SynthesisPayload

def synthesize_ssml(payload: SynthesisPayload, config: dict = None):
    config = config or {}
    speech_config = get_speech_config(api_key=config.get('api_key'), region=config.get('region'))
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat[payload.output_format])

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_ssml_async(payload.ssml).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure SSML synthesis failed: {result.cancellation_details.error_details}")

    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
