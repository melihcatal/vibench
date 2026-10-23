from typing import Dict, Any


def handle_partial_result(transcript_data: Dict[str, Any]) -> Dict[str, Any]:
    """Processes partial and final streaming recognition results."""
    normalized_result = {
        "text": transcript_data["transcript"].strip(),
        "is_final": transcript_data["is_final"],
        "confidence": transcript_data.get("stability", 0.0),
        "words": [],
    }

    if transcript_data["is_final"]:
        normalized_result["words"] = [
            {
                "word": word.word,
                "start_time": word.start_time.total_seconds(),
                "end_time": word.end_time.total_seconds(),
            }
            for word in transcript_data.get("alternatives", [{}])[0].get("words", [])
        ]

    return normalized_result


def aggregate_results(results: list) -> Dict[str, Any]:
    """Aggregates multiple partial results into a single transcript."""
    final_transcript = " ".join(
        result["text"] for result in results if result["is_final"]
    ).strip()

    return {
        "transcript": final_transcript,
        "segments": results,
    }
