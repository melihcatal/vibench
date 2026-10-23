import speech_client
import azure.cognitiveservices.speech as speechsdk


def transcribe_synthesized_audio(audio_file_path: str) -> str:
    """Transcribes synthesized QA samples to verify spoken output using Azure AI Speech."""
    speech_recognizer = speech_client.get_speech_recognizer_client(audio_file_path)

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        raise Exception(f"No speech could be recognized in {audio_file_path}: NoMatch")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        raise Exception(
            f"Speech recognition canceled for {audio_file_path}: {cancellation_details.reason}. Error details: {cancellation_details.error_details}"
        )
    return ""
