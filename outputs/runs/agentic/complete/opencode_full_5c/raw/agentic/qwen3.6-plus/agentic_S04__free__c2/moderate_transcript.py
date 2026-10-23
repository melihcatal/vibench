import sys
import json
from typing import Optional, List, Dict, Any

from speech_models import (
    TranscriptionResult,
    ModerationResult,
    OpenAIConfig,
)
from speech_client import (
    get_transcription_result,
    call_openai_api,
    get_openai_config,
    poll_until_complete,
    get_assemblyai_config,
)


def moderate_transcript_text(
    text: str,
    config: Optional[OpenAIConfig] = None,
) -> ModerationResult:
    if config is None:
        config = get_openai_config()
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    payload = {
        "input": text,
        "model": config.moderation_model,
    }
    response = call_openai_api("moderations", payload, config)
    return ModerationResult.from_openai_response(response, original_text=text)


def moderate_transcript_segments(
    segments: List[Dict[str, Any]],
    text_key: str = "text",
    config: Optional[OpenAIConfig] = None,
) -> List[Dict[str, Any]]:
    if config is None:
        config = get_openai_config()
    moderated_results = []
    for segment in segments:
        text = segment.get(text_key, "")
        if not text:
            moderated_results.append(
                {
                    **segment,
                    "moderation": {
                        "flagged": False,
                        "categories": {},
                        "sanitized_text": text,
                    },
                }
            )
            continue
        mod_result = moderate_transcript_text(text, config)
        moderated_segment = dict(segment)
        moderated_segment["moderation"] = {
            "flagged": mod_result.flagged,
            "categories": mod_result.categories,
            "category_scores": {
                k: round(v, 4) for k, v in mod_result.category_scores.items()
            },
            "sanitized_text": mod_result.sanitized_text,
        }
        moderated_results.append(moderated_segment)
    return moderated_results


def moderate_completed_transcript(
    job_id: str,
    use_utterances: bool = True,
    redact_flagged: bool = True,
) -> Dict[str, Any]:
    assemblyai_config = get_assemblyai_config()
    result = poll_until_complete(job_id, assemblyai_config)
    if use_utterances:
        segments = [
            {
                "text": u.text,
                "speaker": u.speaker,
                "start_ms": u.start,
                "end_ms": u.end,
            }
            for u in result.utterances
        ]
    else:
        segments = [
            {
                "text": w.text,
                "start_ms": w.start,
                "end_ms": w.end,
            }
            for w in result.words
        ]
    moderated_segments = moderate_transcript_segments(segments)
    flagged_count = sum(
        1 for s in moderated_segments if s.get("moderation", {}).get("flagged", False)
    )
    sanitized_segments = []
    for seg in moderated_segments:
        sanitized = dict(seg)
        if redact_flagged and seg.get("moderation", {}).get("flagged", False):
            sanitized["text"] = seg["moderation"]["sanitized_text"]
        sanitized_segments.append(sanitized)
    return {
        "job_id": job_id,
        "total_segments": len(moderated_segments),
        "flagged_segments": flagged_count,
        "safe_to_publish": flagged_count == 0,
        "segments": sanitized_segments,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python moderate_transcript.py <job_id>")
        sys.exit(1)
    job_id = sys.argv[1]
    result = moderate_completed_transcript(job_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
