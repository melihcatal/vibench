# [HELPER] speech_models.py
# Local request/response normalization helpers for Batch Speech-to-Text integrations


class SpeechRequest:
    """Wrapper for constructing provider-specific transcription requests."""

    def __init__(
        self, audio_path: str, diarization: bool = False, timestamps: bool = False
    ):
        self.audio_path = audio_path
        self.diarization = diarization
        self.timestamps = timestamps

    def as_assemblyai_payload(self) -> dict:
        """Return payload dict for AssemblyAI batch transcription."""
        payload = {"audio_url": f"file://{self.audio_path}"}
        if self.diarization:
            # AssemblyAI does not have built-in diarization; placeholder for future extensions
            pass
        if self.timestamps:
            # Request word timestamps via query param (example for Google) - here just a flag
            pass
        return payload

    def as_azure_payload(self) -> dict:
        """Return payload dict for Azure AI Speech SDK (not used in REST calls)."""
        # Placeholder illustrating how one might structure a request object for Azure SDK usage
        return {
            "audio_config": {
                "audio_file_path": self.audio_path,
                "diarization_speaker_count": 5 if self.diarization else None,
            },
            "request_options": {},
        }

    def as_google_payload(self) -> dict:
        """Return payload dict for Google Cloud Speech-to-Text."""
        return {
            "config": {
                "encoding": "LINEAR16",
                "sample_rate_hertz": 16000,
                "language_code": "en-US",
                "enable_word_time_offsets": self.timestamps,
                "diarization_config": {
                    "enable_speaker_diarization": self.diarization,
                    "max_speaker_count": 5,
                },
            }
        }


class SpeechResponse:
    """Normalized response format across providers."""

    def __init__(self, provider_raw: dict):
        self._raw = provider_raw

    @property
    def transcript(self) -> str:
        # AssemblyAI and Google responses have different paths
        if isinstance(self._raw, dict) and "results" in self._raw:
            # Google format
            first_result = self._raw["results"][0]
            if first_result.get("alternatives"):
                return first_result["alternatives"][0]["transcript"]
        if isinstance(self._raw, dict) and "text" in self._raw:
            # AssemblyAI format
            return self._raw["text"]
        if isinstance(self._raw, dict) and "diarization_inference" in self._raw:
            # Azure diarization format (example)
            return self._raw["text"]
        raise ValueError("Unsupported response structure")

    @property
    def words(self) -> list:
        """Flatten word-level timestamps when available."""
        if isinstance(self._raw, dict) and "results" in self._raw:
            # Google word offsets
            words = []
            for result in self._raw["results"]:
                for alt in result.get("alternatives", []):
                    for word in alt.get("words", []):
                        words.append(
                            {
                                "word": word["word"],
                                "start": word["start_time"].seconds
                                + word["start_time"].nanos / 1e9,
                                "end": word["end_time"].seconds
                                + word["end_time"].nanos / 1e9,
                            }
                        )
            return words
        # AssemblyAI already returns words list in its dict
        if isinstance(self._raw, dict) and "words" in self._raw:
            return self._raw["words"]
        raise ValueError("Words not available in response")
