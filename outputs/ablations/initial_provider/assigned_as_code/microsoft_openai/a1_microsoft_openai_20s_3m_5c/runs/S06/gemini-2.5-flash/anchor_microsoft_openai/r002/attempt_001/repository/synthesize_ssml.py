import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import SSMLSynthesisPayload

def synthesize_ssml(payload: SSMLSynthesisPayload):
    speech_config = get_speech_config()
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat[payload.output_format])
    
    audio_config = speechsdk.AudioConfig(use_ synthesized_audio_stream=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    result = speech_synthesizer.speak_ssml_async(payload.ssml).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure SSML synthesis failed: {result.reason}")

    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
