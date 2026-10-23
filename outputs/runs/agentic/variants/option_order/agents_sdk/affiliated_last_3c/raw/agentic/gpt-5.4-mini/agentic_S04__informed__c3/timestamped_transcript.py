from __future__ import annotations

from typing import List, Dict, Any

from speech_client import create_client, normalize_transcript


def timestamped_transcript(audio_url: str, include_words: bool = True) -> List[Dict[str, Any]]:
    client = create_client()
    transcript = client.transcribe(audio_url, config={"speaker_labels": True, "punctuate": True, "format_text": True, "word_boost": []})
    normalized = normalize_transcript(transcript)
    output: List[Dict[str, Any]] = []
    for segment in normalized.segments:
        item: Dict[str, Any] = {"start": segment.start, "end": segment.end, "speaker": segment.speaker, "text": segment.text}
        if include_words:
            item["words"] = segment.words
        output.append(item)
    return output
