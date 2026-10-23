import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class GcsTranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
    model: str = "default"
    features: Optional[List[str]] = None
    output_uri: Optional[str] = None

@dataclasses.dataclass
class GcsTranscriptionJob:
    name: str

@dataclasses.dataclass
class GcsTranscriptionResult:
    transcript: str
    confidence: float
    words: Optional[List[dict]] = None
    speakers: Optional[List[dict]] = None

def normalize_gcs_transcript_response(response: dict) -> List[GcsTranscriptionResult]:
    # This is a placeholder for actual normalization logic.
    # In a real scenario, this function would parse the Google Cloud Speech-to-Text
    # batch transcription result JSON and convert it into a list of GcsTranscriptionResult objects.
    # For now, it returns a dummy result.
    results = []
    if response and "results" in response:
        for res in response["results"]:
            if "alternatives" in res:
                for alt in res["alternatives"]:
                    results.append(GcsTranscriptionResult(
                        transcript=alt.get("transcript", ""),
                        confidence=alt.get("confidence", 0.0),
                        words=alt.get("words"),
                        # In a real scenario, speaker diarization results would be parsed here
                        speakers=None
                    ))
    return results
