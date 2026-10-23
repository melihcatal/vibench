
"""
Define local request, response, and normalization helpers for Batch Speech-to-Text.
This module provides data structures and utility functions to interact with a Batch Speech-to-Text API,
such as Google Cloud Speech-to-Text (e.g., google.cloud.speech_v1p1beta1).
"""

from typing import List, Dict, Any

class BatchTranscriptionRequest:
    """
    Represents a request to the Batch Speech-to-Text API.
    """
    def __init__(self, audio_uri: str, language_code: str = "en-US", config: Dict[str, Any] = None):
        self.audio_uri = audio_uri
        self.language_code = language_code
        self.config = config if config is not None else {}

    def to_json(self) -> Dict[str, Any]:
        """Converts the request object to a dictionary suitable for JSON serialization."""
        return {
            "audio_uri": self.audio_uri,
            "language_code": self.language_code,
            "speech_context": self.config.get("speech_context"),
            "model": self.config.get("model", "default"),
            "enable_automatic_punctuation": self.config.get("enable_automatic_punctuation", False),
            "enable_word_time_offsets": self.config.get("enable_word_time_offsets", False),
        }

class BatchTranscriptionResponse:
    """
    Represents a response from the Batch Speech-to-Text API.
    """
    def __init__(self, raw_response: Dict[str, Any]):
        self.raw_response = raw_response
        self.transcript: str = ""
        self.words: List[Dict[str, Any]] = []
        self._parse_response()

    def _parse_response(self):
        """Parses the raw API response to extract relevant transcription data."""
        results = self.raw_response.get("results", [])
        full_transcript = []
        word_list = []

        for result in results:
            if "alternatives" in result and result["alternatives"]:
                # Assuming the first alternative is the most probable one
                alternative = result["alternatives"][0]
                if "transcript" in alternative:
                    full_transcript.append(alternative["transcript"])
                if "words" in alternative:
                    word_list.extend(alternative["words"])

        self.transcript = " ".join(full_transcript)
        self.words = word_list

    def get_full_transcript(self) -> str:
        """Returns the full transcribed text."""
        return self.transcript

    def get_word_timestamps(self) -> List[Dict[str, Any]]:
        """Returns a list of words with their start and end timestamps."""
        return self.words

def normalize_transcript(transcript_text: str) -> str:
    """
    Applies normalization rules to the transcribed text.
    This is a placeholder function; actual normalization might involve
    punctuation correction, case conversion, removal of filler words, etc.
    """
    # Example normalization: convert to lowercase and strip extra spaces
    return " ".join(transcript_text.lower().split()).strip()
