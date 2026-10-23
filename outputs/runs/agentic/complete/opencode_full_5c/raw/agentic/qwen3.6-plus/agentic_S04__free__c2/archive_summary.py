import sys
import json
from typing import Optional, List, Dict, Any

from speech_models import (
    TranscriptionResult,
    SummaryResult,
    OpenAIConfig,
)
from speech_client import (
    call_openai_api,
    get_openai_config,
    poll_until_complete,
    get_assemblyai_config,
)


def summarize_transcript(
    text: str,
    include_key_points: bool = True,
    include_topics: bool = True,
    include_action_items: bool = True,
    config: Optional[OpenAIConfig] = None,
) -> SummaryResult:
    if config is None:
        config = get_openai_config()
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    requirements = []
    if include_key_points:
        requirements.append("- key_points: A list of the main discussion points")
    if include_topics:
        requirements.append("- topics: A list of topics covered")
    if include_action_items:
        requirements.append("- action_items: A list of action items or decisions made")
    requirements_str = "\n".join(requirements) if requirements else ""
    prompt = (
        "Analyze the following meeting transcript and provide a structured summary.\n"
        f"Return ONLY a valid JSON object with the following keys:\n"
        "- summary: A concise paragraph summarizing the meeting\n"
        f"{requirements_str}\n\n"
        "Transcript:\n"
        f"{text}\n"
    )
    payload = {
        "model": config.summary_model,
        "messages": [
            {
                "role": "system",
                "content": "You are an expert meeting analyst. Return only valid JSON with no markdown formatting.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }
    response = call_openai_api("chat/completions", payload, config)
    return SummaryResult.from_openai_response(response)


def archive_transcription_summary(
    job_id: str,
    include_key_points: bool = True,
    include_topics: bool = True,
    include_action_items: bool = True,
) -> Dict[str, Any]:
    assemblyai_config = get_assemblyai_config()
    transcription = poll_until_complete(job_id, assemblyai_config)
    summary = summarize_transcript(
        transcription.text,
        include_key_points=include_key_points,
        include_topics=include_topics,
        include_action_items=include_action_items,
    )
    speaker_stats = {}
    for utterance in transcription.utterances:
        speaker = utterance.speaker or "unknown"
        if speaker not in speaker_stats:
            speaker_stats[speaker] = {
                "speaker": speaker,
                "utterance_count": 0,
                "total_words": 0,
            }
        speaker_stats[speaker]["utterance_count"] += 1
        speaker_stats[speaker]["total_words"] += len(utterance.text.split())
    return {
        "job_id": job_id,
        "audio_duration_seconds": round(transcription.audio_duration, 2),
        "language": transcription.language_code or "unknown",
        "word_count": len(transcription.text.split()),
        "speaker_count": len(speaker_stats),
        "speaker_statistics": list(speaker_stats.values()),
        "summary": summary.summary,
        "key_points": summary.key_points,
        "topics": summary.topics,
        "action_items": summary.action_items,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python archive_summary.py <job_id>")
        sys.exit(1)
    job_id = sys.argv[1]
    result = archive_transcription_summary(job_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
