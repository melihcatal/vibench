from typing import Dict, Any
import os
import azure.cognitiveservices.speech as speechsdk


class AzureSpeechTranscriber:
    """Transcribe synthesized QA samples to verify spoken output using Azure AI Speech."""

    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.speech_region
        )

    def transcribe(self, audio_bytes: bytes) -> str:
        """Transcribe audio bytes to text."""
        audio_config = speechsdk.audio.AudioConfig(
            stream=speechsdk.audio.PullAudioInputStream(
                self._audio_stream_callback(audio_bytes)
            )
        )
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )
        result = speech_recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            raise Exception("No speech could be recognized")
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            raise Exception(
                f"Speech recognition canceled: {cancellation_details.reason}"
            )

    def _audio_stream_callback(self, audio_bytes: bytes):
        """Callback to stream audio bytes."""

        def stream_callback(audio_buffer: memoryview) -> int:
            nonlocal audio_bytes
            chunk = audio_bytes[: len(audio_buffer)]
            audio_bytes = audio_bytes[len(audio_buffer) :]
            audio_buffer[:] = chunk
            return len(chunk)

        return stream_callback
