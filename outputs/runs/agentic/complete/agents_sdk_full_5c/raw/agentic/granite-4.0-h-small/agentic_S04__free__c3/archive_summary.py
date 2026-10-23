import re
import json
from typing import Dict, Any, List
from speech_models import BatchTranscriptionResult

def summarize_transcript(transcript: BatchTranscriptionResult) -> Dict[str, Any]:
    """Creates a concise summary of a transcription job result.

    Constructs a dictionary containing:
    - total_duration_seconds
    - speaker_summary: count per speaker
    - average_confidence
    - segment_count
    - top_keywords: top 5 nouns (simple tokenization)

    Args:
        transcript (BatchTranscriptionResult): API response JSON.

    Returns:
        dict: Summary dictionary.
    """
    results = transcript.get("results", [])
    if not results:
        raise ValueError("Empty transcription result.")

    # Duration calculation (audio_total_time_ms field at top level of result)
    total_ms = results[0].get("audio_total_time_ms", 0)
    total_seconds = total_ms / 1000.0

    # Speaker count
    speakers = set()
    total_confidence = 0.0
    segment_count = 0
    all_words = []
    for result in results:
        segment_items = result.get("items", [])
        segment_count += len(segment_items)
        for seg in segment_items:
            speakers.add(seg.get("speaker_labels", [None])[0])
            total_confidence += seg.get("confidence", 0.0)
            # Simple word extraction (letters only, lowercased)
            words = re.findall(r"[A-Za-z']{2,}", seg.get("content", ""))
            all_words.extend([w.lower() for w in words])

    avg_confidence = total_confidence / segment_count if segment_count else 0.0
    speaker_summary = {spk: speakers.count(spk) for spk in speakers}

    # Simple keyword extraction: most common non-stopwords
    stopwords = {
        "the", "and", "of", "to", "a", "in", "that", "is", "it", "for", "on", "with",
        "as", "was", "by", "at", "be", "this", "but", "from", "or", "an", "are"
    }
    word_counts = {}
    for w in all_words:
        if w not in stopwords:
            word_counts[w] = word_counts.get(w, 0) + 1
    # Get top 5 keywords sorted descending by frequency
    top_keywords = sorted(word_counts.items(), key=lambda kv: kv[1], reverse=True)[:5]
    keywords = [kw for kw, count in top_keywords]

    summary = {
        "total_duration_sec": total_seconds,
        "speaker_summary": speaker_summary,
        "average_confidence": avg_confidence,
        "segment_count": segment_count,
        "top_keywords": keywords
    }
    return summary

# CLI helper
if __name__ == "__main__":
    import sys, json
    if len(sys.argv) != 2:
        print("Usage: python archive_summary.py <result_json_file>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    summary = summarize_transcript(raw)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
