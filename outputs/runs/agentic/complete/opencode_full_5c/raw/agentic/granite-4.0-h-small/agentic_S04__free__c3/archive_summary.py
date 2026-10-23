# archive_summary.py


def summarize_transcript(segments: list) -> str:
    """Generate a concise summary of a timestamped transcript."""
    # Join segment texts and create a short summary using basic heuristics
    full_text = " ".join(seg["text"] for seg in segments)
    # Simple keyword extraction as placeholder
    keywords = ["meeting", "discussion", "summary", "action", "item"]
    summary = " ".join(word for word in full_text.split() if word.lower() in keywords)
    return summary or "Brief summary not available"


if __name__ == "__main__":
    import sys, json

    segments = eval(sys.argv[1])  # expects JSON string argument
    summary = summarize_transcript(segments)
    print(json.dumps({"summary": summary}))
