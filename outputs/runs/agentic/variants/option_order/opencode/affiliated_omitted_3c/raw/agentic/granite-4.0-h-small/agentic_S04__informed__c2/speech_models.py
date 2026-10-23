# HELPER: speech_models.py

# Local request/response normalization utilities for batch speech-to-text
import json
from typing import Any, Dict, List

class TranscriptionResult:
    """Normalized container for a transcription result from any provider."""
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        self._transcript = None
        self._timestamps = None
        self._speakers = None
        self._diarization = None

    @property
    def transcript(self) -> str:
        """Unified transcript string."""
        if self._transcript is None:
            # Attempt to locate transcript in known structures
            if "transcript" in self.raw:
                self._transcript = self.raw["transcript"]
            elif "results" in self.raw and self.raw["results"]:
                # Amazon Transcribe / Google style
                alt = self.raw["results"][0]["alternatives"][0]
                self._transcript = alt.get("transcript", "")
        return self._transcript

    @property
    def timestamps(self) -> List[Dict[str, float]]:
        """List of word-level timestamps {word, start, end}."""
        if self._timestamps is None:
            # Try common keys
            if "timestamps" in self.raw:
                self._timestamps = self.raw["timestamps"]
            elif "results" in self.raw and self.raw["results"]:
                alt = self.raw["results"][0]["alternatives"][0]
                if "items" in alt:
                    self._timestamps = [
                        {
                            "word": item.get("content", ""),
                            "start": item.get("start_time", 0.0),
                            "end": item.get("end_time", 0.0),
                        }
                        for item in alt["items"]
                        if item.get("type") == "word"
                    ]
        return self._timestamps

    @property
    def diarization(self) -> List[Dict[str, Any]]:
        """Speaker diarization segments {speaker, start, end}."""
        if self._diarization is None:
            # Google Speech returns `words[i].speaker_tag` and timestamps
            if "results" in self.raw and self.raw["results"]:
                results = self.raw["results"]
                self._diarization = []
                for result in results:
                    for word in result["alternatives"][0]["words"]:
                        tag = word.get("speaker_tag")
                        if tag is not None:
                            start = word["start_time"].seconds + word["start_time"].nanos / 1e9
                            # Use next word's start as end time (approx.)
                            end = (
                                results[results.index(result) + 1]["alternatives"][0]["words"]
                                if results.index(result) + 1 < len(results)
                                else start + 1.0
                            )[0]["start_time"].seconds
                            + results[results.index(result) + 1]["alternatives"][0]["words"][0][
                                "start_time"
                            ].nanos
                            / 1e9
                            )
                            self._diarization.append({"speaker": tag, "start": start, "end": end})
        return self._diarization

    def to_dict(self) -> Dict[str, Any]:
        """Return a clean dict with unified fields."""
        return {
            "transcript": self.transcript,
            "timestamps": self.timestamps,
            "diarization": self.diarization,
        }
