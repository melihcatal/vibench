# speech_client.py
import os
from typing import Dict, Any

# Helper utilities for constructing requests, parsing responses, and logging


class SpeechClient:
    """Local helper class providing convenience wrappers around external SDKs."""

    def __init__(self):
        # Load credentials from environment (example for AssemblyAI)
        self.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        # Initialize provider SDKs (only AssemblyAI used in examples)
        self.assemblyai = assemblyai.Client(token=self.api_key)  # type: ignore

    def build_transcription_payload(
        self, file_path: str, language: str = "en-US"
    ) -> Dict[str, Any]:
        """Prepares a transcription request payload."""
        return {
            "file": file_path,
            "language": language,
        }

    def build_diarization_payload(
        self, file_path: str, num_speakers: int = 2
    ) -> Dict[str, Any]:
        """
        Prepares a diarization request payload.
        """
        return {
            "file": file_path,
            "num_speakers": num_speakers,
        }

    def extract_transcript(self, raw_result: Dict[str, Any]) -> str:
        """Extracts transcript text from a provider's raw result."""
        return raw_result.get("transcript", "")

    def normalize_diarized_response(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalizes diarization results into a consistent schema.
        """
        speakers = raw.get("segments", [])
        return {
            "speakers": [
                {"id": s["speaker_id"], "segments": s["segments"]} for s in speakers
            ]
        }

    def parse_timestamps(self, raw: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parses timestamps into a list of dictionaries."""
        words = raw.get("words", [])
        return [
            {"start": w["start"], "end": w["end"], "text": w["word"]} for w in words
        ]


# Singleton instance used across the same-scenario files
speech_client = SpeechClient()
