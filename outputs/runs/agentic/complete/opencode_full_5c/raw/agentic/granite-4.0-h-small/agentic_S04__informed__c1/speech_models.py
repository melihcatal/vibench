from typing import TypedDict, List
import json


class Word(TypedDict):
    text: str
    start_time: float
    end_time: float


class Speaker(TypedDict):
    id: int
    name: str
    start_time: float
    end_time: float


class TranscriptResult(TypedDict):
    text: str
    words: List[Word]
    speakers: List[Speaker]


def normalize_assemblyai_transcript(resp: dict) -> TranscriptResult:
    """
    Convert AssemblyAI SDK response into the normalized TranscriptResult structure.
    """
    # Expected keys in resp: text, words, speakers
    return {
        "text": resp["text"],
        "words": [
            {
                "text": w["text"],
                "start_time": w["start"],
                "end_time": w["end"],
            }
            for w in resp["words"]
        ],
        "speakers": [
            {
                "id": s["id"],
                "name": s.get("name", "Speaker"),
                "start_time": s["start"],
                "end_time": s["end"],
            }
            for s in resp.get("speakers", [])
        ],
    }


def parse_ibm_stt_response(resp: str) -> str:
    """
    Simple parser for IBM Watson STT JSON output, returning only the transcript text.
    """
    data = json.loads(resp)
    return data["results"][0]["alternatives"][0]["transcript"]
