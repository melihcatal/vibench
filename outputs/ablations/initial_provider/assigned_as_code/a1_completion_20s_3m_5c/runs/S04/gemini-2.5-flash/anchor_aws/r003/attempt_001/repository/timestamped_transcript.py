import json
import urllib.request
from typing import List, Dict, Any

from speech_models import TranscriptSegment

def timestamped_transcript(transcript_uri: str) -> List[TranscriptSegment]:
    # Fetch the content from the S3 URI
    with urllib.request.urlopen(transcript_uri) as url:
        data = json.loads(url.read().decode())

    segments = []
    if "results" in data and "speaker_labels" in data["results"]:
        items = data["results"]["items"]
        speaker_labels = data["results"]["speaker_labels"]["segments"]

        # This is a simplified approach. A more robust solution would iterate through items
        # and align them with speaker labels. For demonstration, we'll process speaker segments.
        for s_label in speaker_labels:
            segment_content = []
            segment_words = []
            for item_index in range(s_label["start_item_index"], s_label["end_item_index"] + 1):
                item = items[item_index]
                if item["type"] == "pronunciation":
                    segment_content.append(item["alternatives"][0]["content"])
                    segment_words.append({
                        "word": item["alternatives"][0]["content"],
                        "start_time": item["start_time"],
                        "end_time": item["end_time"]
                    })
            segments.append(TranscriptSegment(
                start_time=float(s_label["start_time"]),
                end_time=float(s_label["end_time"]),
                speaker_label=s_label["speaker_label"],
                content=" ".join(segment_content),
                words=segment_words
            ))
    elif "results" in data and "items" in data["results"]:
        # Non-diarized transcript, extract word-level timestamps directly
        current_segment_content = []
        current_segment_words = []
        current_segment_start_time = None
        current_segment_end_time = None

        for item in data["results"]["items"]:
            if item["type"] == "pronunciation":
                word = item["alternatives"][0]["content"]
                start_time = float(item["start_time"])
                end_time = float(item["end_time"])

                if current_segment_start_time is None:
                    current_segment_start_time = start_time
                current_segment_end_time = end_time

                current_segment_content.append(word)
                current_segment_words.append({
                    "word": word,
                    "start_time": start_time,
                    "end_time": end_time
                })
            elif item["type"] == "punctuation":
                # Punctuation marks are usually associated with the preceding word/segment
                # For simplicity, we'll append to the current segment content
                current_segment_content.append(item["alternatives"][0]["content"])

            # Simple heuristic for segmenting: if a pause or end of utterance
            # A more advanced approach would use more sophisticated segmentation logic
            if item["type"] == "punctuation" and item["alternatives"][0]["content"] in [".", "?", "!"] and current_segment_content:
                segments.append(TranscriptSegment(
                    start_time=current_segment_start_time if current_segment_start_time is not None else 0.0,
                    end_time=current_segment_end_time if current_segment_end_time is not None else 0.0,
                    speaker_label="speaker_0", # Default speaker for non-diarized
                    content="".join(current_segment_content),
                    words=current_segment_words
                ))
                current_segment_content = []
                current_segment_words = []
                current_segment_start_time = None
                current_segment_end_time = None
        
        # Add any remaining segment after the loop
        if current_segment_content:
            segments.append(TranscriptSegment(
                start_time=current_segment_start_time if current_segment_start_time is not None else 0.0,
                end_time=current_segment_end_time if current_segment_end_time is not None else 0.0,
                speaker_label="speaker_0",
                content="".join(current_segment_content),
                words=current_segment_words
            ))

    return segments
