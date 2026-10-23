import dataclasses
from typing import List, Tuple
from google.protobuf import json_format
from google.cloud.speech_v1p1beta1 import StreamingRecognizeResponse, StreamingRecognitionResult, WordInfo

# Model for word-level timestamps (used by Google Speech)
@dataclasses.dataclass
class WordInfoWrapper:
    word: str
    start_time_seconds: float
    end_time_seconds: float
    confidence: float = None
    # Additional fields can be added as needed

@dataclasses.dataclass
class SpeechResult:
    is_partial: bool
    transcript: str
    word_infos: List[WordInfoWrapper] = dataclasses.field(default_factory=list)
    confidence: float = None
    # Future extensions: speaker labels, diarization, etc.

# Helper to convert streaming response protobuf to SpeechResult objects
# This file is a local helper; production code would import it from speech_client.py

def proto_to_speech_result(response: StreamingRecognizeResponse) -> List[Tuple[bool, str]]:
    """Convert a StreamingRecognizeResponse to a list of (is_partial, transcript) tuples.","""
    results = []
    for result in response.results:
        if result.alternatives:
            alt = result.alternatives[0]
            transcript = alt.transcript
            is_partial = not result.is_final
            # Optional: parse WordInfo into WordInfoWrapper list
            word_infos = []
            for w in alt.words:
                word_infos.append(
                    WordInfoWrapper(
                        word=w.word,
                        start_time_seconds=w.start_time.seconds + w.start_time.nanos / 1e9,
                        end_time_seconds=w.end_time.seconds + w.end_time.nanos / 1e9,
                        confidence=w.confidence,
                    )
                )
            results.append((is_partial, transcript, word_infos))
            # Keep word_infos for later use if needed
    return results

# Example utility for IBM Watson partial results (simplified JSON payload)
# IBM Watson streaming responses are JSON lines; we expose a function to parse them.
# def watson_partial_handler(raw_json: str) -> Tuple[bool, str]:
#     payload = json.loads(raw_json)
#     if 'results' in payload and payload['results']:
#         # Example field names; adjust to actual schema
#         partial = payload['results'][0].get('partial', True)
#         text = payload['results'][0].get('alternatives', [{}])[0].get('transcript', '')
#         return partial, text
#     return False, ''
