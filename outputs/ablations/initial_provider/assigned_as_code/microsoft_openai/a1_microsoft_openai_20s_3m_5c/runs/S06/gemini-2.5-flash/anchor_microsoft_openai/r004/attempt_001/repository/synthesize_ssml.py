import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import TextToSpeechConfig, SynthesisInput

def synthesize_ssml(payload: SynthesisInput, config: TextToSpeechConfig) -> dict:
    speech_config = get_speech_config(config)
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = speech_synthesizer.speak_ssml_async(payload.ssml).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        raise RuntimeError(f"Azure SSML synthesis failed: {result.cancellation_details.reason}")
        
    return {'audio_bytes': result.audio_data, 'content_type': 'audio/mpeg'}
