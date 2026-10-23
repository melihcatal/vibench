# [LATER-STEP] archive_summary.py
import os
from speech_models import extract_transcript, normalize_result
from typing import List, Dict

def archive_summary(transcript_result: Dict[str, Any], max_words: int = 150) -> Dict[str, Any]:
    """
    Produce a concise summary of the transcription suitable for archival metadata.
    
    Args:
        transcript_result (Dict): Normalized result from speech_models.normalize_result.
        max_words (int): Target word count for the summary.
    
    Returns:
        Dict: Summary text and word count.
    """
    original = transcript_result.get("transcript", "")
    words = original.split()
    if len(words) <= max_words:
        summary = original
    else:
        summary = " ".join(words[:max_words]) + " ..."
    return {
        "job_id": transcript_result.get("job_id", "unknown"),
        "status": transcript_result.get("status", "unknown"),
        "summary": summary,
        "summary_word_count": len(summary.split()),
        "total_words": len(words)
    }

if __name__ == "__main__":
    import json, sys
    if len(sys.argv) < 2:
        print("Usage: python archive_summary.py <result_json_file> [max_words]")
        sys.exit(1)
    file_path = sys.argv[1]
    max_words = int(sys.argv[2]) if len(sys.argv) > 2 else 150
    with open(file_path, "r") as f:
        result = json.load(f)
    norm = normalize_result(result)
    out = archive_summary(norm, max_words)
    print(json.dumps(out, ensure_ascii=False, indent=2))
