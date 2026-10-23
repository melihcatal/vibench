import azure.cognitiveservices.speech as speechsdk
from speech_client import AzureSpeechClient
from speech_models import SynthesisSSMLInput, SynthesisOutput

def synthesize_ssml(input: SynthesisSSMLInput) -> SynthesisOutput:
    speech_config = AzureSpeechClient()
    speech_config.speech_synthesis_voice_name = input.voice_name
    speech_config.speech_synthesis_language = input.locale # Set locale for SSML processing

    audio_config = speechsdk.audio.AudioOutputConfig(use_ default_speaker=False, stream_output=True)

    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_ssml_async(input.ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return SynthesisOutput(audio_content=result.audio_data, audio_format="wav") # Azure typically returns WAV
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}")
    else:
        raise Exception(f"Speech synthesis failed: {result.reason}")
