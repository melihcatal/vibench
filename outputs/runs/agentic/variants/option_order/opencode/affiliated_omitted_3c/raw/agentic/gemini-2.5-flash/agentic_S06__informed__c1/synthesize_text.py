import speech_client
import azure.cognitiveservices.speech as speechsdk


def synthesize_text_to_audio(text: str, voice_name: str = "en-US-JennyNeural") -> bytes:
    """Synthesizes plain text to an audio byte stream using Azure Speech TTS."""
    speech_synthesizer = speech_client.get_speech_synthesizer_client()
    speech_synthesizer.speech_config.speech_synthesis_voice_name = voice_name

    result = speech_synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(
            f"Speech synthesis canceled: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        )
    return b""
