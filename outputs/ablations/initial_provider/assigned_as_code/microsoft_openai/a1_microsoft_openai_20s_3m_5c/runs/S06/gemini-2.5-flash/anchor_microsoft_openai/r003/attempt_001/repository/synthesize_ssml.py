import azure.cognitiveservices.speech as speechsdk
from speech_client import AzureSpeechClient
from speech_models import SynthesisRequest, SynthesisResponse, SpeechSynthesisConfig

def synthesize_ssml(payload: SynthesisRequest, config: SpeechSynthesisConfig) -> SynthesisResponse:
    speech_client = AzureSpeechClient(config)
    synthesizer = speech_client.get_synthesizer()

    result = synthesizer.speak_ssml_async(payload.ssml).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure speech synthesis failed: {result.cancellation_details.reason}")

    return SynthesisResponse(audio_bytes=result.audio_data, content_type='audio/mpeg')
