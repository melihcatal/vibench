import azure.cognitiveservices.speech as speechsdk
from speech_client import get_speech_config
from speech_models import SynthesisSSMLRequest

def synthesize_ssml(request: SynthesisSSMLRequest) -> bytes:
    speech_config = get_speech_config()
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat(request.output_format))

    audio_config = speechsdk.audio.AudioOutputConfig(use_ Albertiudio_stream=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_ssml_async(request.ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")
