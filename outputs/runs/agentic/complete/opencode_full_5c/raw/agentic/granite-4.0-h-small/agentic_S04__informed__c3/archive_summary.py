import json
from typing import List, Dict
from speech_models import SummarizationRequest, SummarizationResponse

# Placeholder: using a simple local function to demonstrate summarization step
# In a real scenario, replace with an LLM inference call (e.g., watsonx.ai, OpenAI, etc.)


def generate_summary(segments: List[Dict[str, Any]], max_length: int = 200) -> str:
    """Generate a concise summary from transcript segments.

    Args:
        segments (List[Dict]): List of segment dicts with 'alternatives' list of strings.
        max_length (int): Maximum characters for the summary.

    Returns:
        str: Summarized text.
    """
    # Extract the first alternative of each segment for simplicity
    text = " ".join(
        segment["alternatives"][0] for segment in segments if segment["alternatives"]
    )
    # Very naive summarization: truncate to max_length
    return (text[:max_length] + "...") if len(text) > max_length else text


def summarize_transcription(
    transcript_segments: List[Dict[str, Any]],
) -> SummarizationResponse:
    raw_summary = generate_summary(transcript_segments, max_length=250)
    return SummarizationResponse(summary=raw_summary)


# Simple CLI wrapper for testing
if __name__ == "__main__":
    sample_segments = [
        {
            "alternatives": ["This is the first sentence of the meeting."],
            "start_time": "00:00:01",
        },
        {
            "alternatives": ["The second part discusses project timeline."],
            "start_time": "00:05:30",
        },
    ]
    result = summarize_transcription(sample_segments)
    print(json.dumps({"summary": result.summary}, indent=2))
