import os
import azure.cognitiveservices.speech as speechsdk


def transcribe_audio_from_file(audio_file_path: str, language: str = "en-US") -> str:
    """
    Transcribes synthesized QA samples from an audio file using Azure AI Speech-to-Text.
    Requires AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables to be set.
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not service_region:
        raise ValueError(
            "AZURE_SPEECH_KEY or AZURE_SPEECH_REGION environment variable not set."
        )

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=service_region
    )
    speech_config.speech_recognition_language = language

    audio_config = speechsdk.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            raise RuntimeError(
                f"Speech recognition canceled due to error: {cancellation_details.error_details}"
            )
        return "Speech recognition canceled."
    return "Unknown transcription error."
