import speech_client
import azure.cognitiveservices.speech as speechsdk


def synthesize_ssml_to_audio(ssml: str) -> bytes:
    """Synthesizes SSML to an audio byte stream using Azure Speech TTS."""
    speech_synthesizer = speech_client.get_speech_synthesizer_client()

    result = speech_synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(
            f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        )
    return b""
