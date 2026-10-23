import os
import time
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.operation import Operation
from typing import Optional

from speech_models import TranscriptionConfig, TranscriptionAudio, TranscriptionResponse


class SpeechClient:
    """Client for interacting with Google Cloud Speech-to-Text API."""

    def __init__(self):
        # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            # This is a placeholder. In a real scenario, you'd handle authentication
            # more robustly, e.g., using default credentials or service account key.
            print(
                "WARNING: GOOGLE_APPLICATION_CREDENTIALS not set. "
                "Using default client initialization, which may fail without proper auth."
            )
        self._client = speech.SpeechClient()

    def _build_recognition_config(
        self, config: TranscriptionConfig
    ) -> speech.RecognitionConfig:
        """Builds a Google Cloud Speech-to-Text RecognitionConfig from a TranscriptionConfig."""
        speaker_diarization_config = None
        if config.enable_speaker_diarization:
            speaker_diarization_config = speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=True,
                min_speaker_count=config.diarization_speaker_count or 1,
                max_speaker_count=config.diarization_speaker_count
                or 6,  # Default max if not specified
            )

        return speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.FLAC,  # Assuming FLAC for batch
            sample_rate_hertz=16000,  # Common sample rate for speech
            language_code=config.language_code,
            enable_automatic_punctuation=config.enable_automatic_punctuation,
            enable_word_time_offsets=config.enable_word_time_offsets,
            model=config.model,
            use_enhanced=True,  # Use enhanced models for better accuracy
            diarization_config=speaker_diarization_config,
        )

    def _build_recognition_audio(
        self, audio: TranscriptionAudio
    ) -> speech.RecognitionAudio:
        """Builds a Google Cloud Speech-to-Text RecognitionAudio from a TranscriptionAudio."""
        return speech.RecognitionAudio(uri=audio.uri)

    def submit_long_running_recognize(
        self, audio: TranscriptionAudio, config: TranscriptionConfig
    ) -> Operation:
        """Submits an audio file for long-running batch transcription."""
        recognition_config = self._build_recognition_config(config)
        recognition_audio = self._build_recognition_audio(audio)

        operation = self._client.long_running_recognize(
            config=recognition_config, audio=recognition_audio
        )
        return operation

    def poll_operation_until_done(
        self, operation_name: str, timeout: Optional[int] = None
    ) -> TranscriptionResponse:
        """Polls a long-running operation until it's done and returns the transcription response."""
        operation = self._client.get_operation(operation_name)
        response = operation.result(timeout=timeout)

        # Convert the Google Cloud Speech response to our internal TranscriptionResponse model
        transcription_response = TranscriptionResponse(uri=operation.metadata.uri)
        for result in response.results:
            alternatives = []
            for alternative in result.alternatives:
                words = []
                for word_info in alternative.words:
                    words.append(
                        TranscriptionResponse.WordInfo(
                            word=word_info.word,
                            start_time=word_info.start_time.seconds
                            + word_info.start_time.nanos * 1e-9,
                            end_time=word_info.end_time.seconds
                            + word_info.end_time.nanos * 1e-9,
                            speaker_tag=word_info.speaker_tag
                            if hasattr(word_info, "speaker_tag")
                            else None,
                        )
                    )
                alternatives.append(
                    TranscriptionResponse.Alternative(
                        transcript=alternative.transcript,
                        confidence=alternative.confidence,
                        words=words,
                    )
                )
            transcription_response.results.append(
                TranscriptionResponse.Result(
                    alternatives=alternatives,
                    channel_tag=result.channel_tag
                    if hasattr(result, "channel_tag")
                    else None,
                )
            )

        return transcription_response

    def get_operation(self, operation_name: str) -> Operation:
        """Retrieves a long-running operation by its name."""
        return self._client.get_operation(operation_name)
