# [HELPER] speech_client.py
# Local helper utilities for Batch Speech-to-Text using Azure AI Speech SDK

import os
import azure.cognitiveservices.speech as speechsdk
from typing import Optional, Dict, Any

# Load Azure credentials from environment (you can extend to load from a config file)
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

if not AZURE_SPEECH_KEY:
    raise RuntimeError("Environment variable AZURE_SPEECH_KEY must be set to your Azure Speech subscription key.")


class SpeechTranscriber:
    """Helper class to encapsulate batch transcription operations.

    Provides convenient methods for submitting, polling, and retrieving results.
    """
    def __init__(self, subscription_key: str = AZURE_SPEECH_KEY, region: str = AZURE_SPEECH_REGION):
        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        self.transcription_client: Optional[speechsdk.transcription.TranscriptionClient] = None

    def _start_client(self):
        if not self.transcription_client:
            self.transcription_client = speechsdk.transcription.TranscriptionClient(self.speech_config)

    def submit_transcription(self, audio_file_path: str, language: str = "en-US") -> str:
        """Submits a batch transcription request.
        Returns the generated job_id.
        """
        self._start_client()
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        transcription_config = speechsdk.TranscriptionConfiguration(language=language)
        job_id = self.transcription_client.start_transcription_from_audio(audio_config, transcription_config)
        return job_id

    def poll_transcription(self, job_id: str) -> str:
        """Polls the transcription service until completion and returns the transcript text.
        """
        self._start_client()
        result = self.transcription_client.get_transcription_result(job_id)
        while result.status != speechsdk.transcription.TranscriptionStatus.Completed:
            # Simple poll with short sleep
            import time
            time.sleep(1)
            result = self.transcription_client.get_transcription_result(job_id)
        return result.transcript_text

    def diarized_transcription(self, audio_file_path: str, speaker_count: int = 2, language: str = "en-US") -> str:
        """Submits batch transcription with speaker diarization.
        Returns the diarized transcript text.
        """
        self._start_client()
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        transcription_config = speechsdk.TranscriptionConfiguration(language=language)
        transcription_config.enable_diarization = True
        transcription_config.number_of_speakers = speaker_count
        job_id = self.transcription_client.start_transcription_from_audio(audio_config, transcription_config)
        result = self.transcription_client.get_transcription_result(job_id)
        while result.status != speechsdk.transcription.TranscriptionStatus.Completed:
            import time
            time.sleep(1)
            result = self.transcription_client.get_transcription_result(job_id)
        return result.transcript_text

    def timestamped_transcription(self, audio_file_path: str, language: str = "en-US") -> str:
        """Transcribes audio and extracts word-level timestamps.
        Returns a string where each line is \"word|start|duration\".
        """
        self._start_client()
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        result = speech_recognizer.recognize_once()
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            words = result.get_wrd()  # List of tuples (word, start, duration, confidence)
            return "\\n".join(f"{w[0]}|{w[1]}|{w[2]}" for w in words)
        else:
            return "Transcription failed."
