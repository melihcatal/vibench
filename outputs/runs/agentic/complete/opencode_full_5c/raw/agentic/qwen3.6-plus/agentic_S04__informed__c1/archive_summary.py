import os
from dataclasses import dataclass, field
from typing import List, Optional
import dashscope
from dashscope import Generation

from speech_models import TranscriptSegment, TranscriptSegments


@dataclass
class ArchiveSummary:
    summary: str
    key_topics: List[str]
    action_items: List[str]
    participant_count: int
    total_segments: int


def summarize_transcript(
    segments: TranscriptSegments,
    api_key: str = None,
    model: str = "qwen-turbo",
    max_tokens: int = 1024,
) -> ArchiveSummary:
    if api_key is None:
        api_key = os.environ.get("DASHSCOPE_API_KEY", "")

    dashscope.api_key = api_key

    full_text = "\n".join(
        f"[{seg.speaker}] {seg.text}" for seg in segments.segments if seg.text.strip()
    )

    prompt = (
        "You are an assistant that summarizes meeting transcripts. "
        "Provide a concise summary, list the key topics discussed, "
        "and extract any action items mentioned. "
        "Format your response as JSON with keys: summary, key_topics, action_items.\n\n"
        f"Transcript:\n{full_text}"
    )

    response = Generation.call(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful meeting summary assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        result_format="message",
        max_tokens=max_tokens,
    )

    output_text = response.output.choices[0].message.content

    import json

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        parsed = {
            "summary": output_text,
            "key_topics": [],
            "action_items": [],
        }

    unique_speakers = set(seg.speaker for seg in segments.segments if seg.speaker)

    return ArchiveSummary(
        summary=parsed.get("summary", output_text),
        key_topics=parsed.get("key_topics", []),
        action_items=parsed.get("action_items", []),
        participant_count=len(unique_speakers),
        total_segments=segments.total_segments,
    )


if __name__ == "__main__":
    sample = TranscriptSegments(
        segments=[
            TranscriptSegment(
                index=0,
                speaker="Speaker A",
                text="Welcome everyone. Let us review the Q4 targets.",
                start_ms=0,
                end_ms=5000,
            ),
            TranscriptSegment(
                index=1,
                speaker="Speaker B",
                text="I will prepare the budget report by Friday.",
                start_ms=5500,
                end_ms=9000,
            ),
            TranscriptSegment(
                index=2,
                speaker="Speaker A",
                text="Great. Speaker C, please handle the client outreach.",
                start_ms=9500,
                end_ms=14000,
            ),
        ],
        total_segments=3,
    )
    summary = summarize_transcript(sample)
    print(f"Summary: {summary.summary}")
    print(f"Topics: {summary.key_topics}")
    print(f"Actions: {summary.action_items}")
