from typing import List, Tuple
from google.cloud.speech_v1p1beta1 import SpeechRecognitionAlternative, SpeechRecognitionResult

# ---------------------------------------------------------------------------
# HELPER: speech_models.py                                                 #
# Contains helper classes / functions for normalizing recognition results,
# handling alternatives, and extracting timestamps (if provided).
# ---------------------------------------------------------------------------

def normalize_transcript(alternative: SpeechRecognitionAlternative) -> str:
    """
    Returns a cleaned transcript string.
    - Strips leading/trailing whitespace
    - Collapses multiple spaces
    - Removes null characters
    """
    txt = alternative.transcript.strip().replace('\00', '')
    return ' '.join(txt.split())

# If word-level timestamps are requested, this extracts them
def extract_words_with_times(
    result: SpeechRecognitionResult,
) -> List[Tuple[str, float, float]]:
    """Return list of (word, start_time_sec, end_time_sec) for the first alternative."""
    words = []
    for word_info in result.alternatives[0].words:
        word = word_info.word
        start = word_info.start_time.seconds + word_info.start_time.nanos / 1e9
        end = word_info.end_time.seconds + word_info.end_time.nanos / 1e9
        words.append((word, start, end))
    return words

# Simple utility to merge duplicate consecutive words (rare in streaming)
def deduplicate_transcript(transcript: str) -> str:
    words = transcript.split()
    deduped = []
    for w in words:
        if not deduped or w != deduped[-1]:
            deduped.append(w)
    return ' '.join(deduped)
