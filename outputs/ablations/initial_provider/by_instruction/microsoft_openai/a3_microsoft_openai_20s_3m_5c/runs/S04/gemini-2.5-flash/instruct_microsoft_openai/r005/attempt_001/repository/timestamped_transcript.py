import json
from typing import List, Dict, Any

def get_timestamped_segments(transcription_result_json: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parses the JSON output of an Azure Batch Speech-to-Text transcription job
    and extracts word-level timestamps.

    Args:
        transcription_result_json: The full JSON response from a completed
                                   Azure Batch Speech-to-Text transcription result file.

    Returns:
        A list of dictionaries, where each dictionary represents a word
        with its text, offset (start time), and duration.
    """
    timestamped_words = []

    # The structure of the result JSON includes 'recognizedPhrases' for batch transcriptions.
    # Each phrase contains an 'nBest' array, and within the best option, a 'words' array.
    recognized_phrases = transcription_result_json.get("recognizedPhrases", [])

    for phrase in recognized_phrases:
        n_best = phrase.get("nBest", [])
        if n_best:
            best_option = n_best[0] # Take the top (best) recognition alternative
            words = best_option.get("words", [])
            for word_info in words:
                word_text = word_info.get("word")
                offset = word_info.get("offset") # in milliseconds
                duration = word_info.get("duration") # in milliseconds
                
                if word_text and offset is not None and duration is not None:
                    timestamped_words.append({
                        "word": word_text,
                        "offset_ms": offset,
                        "duration_ms": duration
                    })
    return timestamped_words

if __name__ == "__main__":
    # Example usage: Simulate a transcription result JSON
    # In a real scenario, you would load this from the file returned by a polling mechanism
    # like in poll_transcription.py.
    sample_transcript_json = {
        "recognizedPhrases": [
            {
                "channel": 0,
                "speaker": 1, # Example for diarization
                "nBest": [
                    {
                        "confidence": 0.95,
                        "lexical": "hello world this is a test",
                        "itn": "hello world this is a test",
                        "maskedITN": "hello world this is a test",
                        "display": "Hello world, this is a test.",
                        "words": [
                            {"word": "Hello", "offset": 500000, "duration": 200000},
                            {"word": "world", "offset": 750000, "duration": 300000},
                            {"word": "this", "offset": 1100000, "duration": 150000},
                            {"word": "is", "offset": 1300000, "duration": 100000},
                            {"word": "a", "offset": 1450000, "duration": 50000},
                            {"word": "test", "offset": 1550000, "duration": 300000}
                        ]
                    }
                ]
            },
            {
                "channel": 0,
                "speaker": 2, # Example for diarization
                "nBest": [
                    {
                        "confidence": 0.92,
                        "lexical": "and another sentence",
                        "itn": "and another sentence",
                        "maskedITN": "and another sentence",
                        "display": "And another sentence.",
                        "words": [
                            {"word": "And", "offset": 2000000, "duration": 100000},
                            {"word": "another", "offset": 2150000, "duration": 250000},
                            {"word": "sentence", "offset": 2450000, "duration": 400000}
                        ]
                    }
                ]
            }
        ]
    }

    timestamped_results = get_timestamped_segments(sample_transcript_json)
    if timestamped_results:
        print("Timestamped Transcript:")
        for item in timestamped_results:
            print(f"  Word: {item['word']}, Offset: {item['offset_ms']}ms, Duration: {item['duration_ms']}ms")
    else:
        print("No timestamped words found.")

