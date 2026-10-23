import sys
import json
from typing import Optional, List, Dict, Any

from speech_models import (
    TranscriptionResult,
    TranslationResult,
    OpenAIConfig,
)
from speech_client import (
    get_transcription_result,
    call_openai_api,
    get_openai_config,
    poll_until_complete,
    get_assemblyai_config,
)


def translate_transcript_segments(
    segments: List[Dict[str, Any]],
    target_language: str,
    source_language: Optional[str] = None,
    config: Optional[OpenAIConfig] = None,
) -> TranslationResult:
    if config is None:
        config = get_openai_config()
    if not config.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    segment_texts = [seg.get("text", "") for seg in segments if seg.get("text")]
    if not segment_texts:
        return TranslationResult(
            segments=[],
            target_language=target_language,
            source_language=source_language or "unknown",
        )
    source_lang = source_language or "auto-detect"
    prompt = (
        f"Translate the following text segments from {source_lang} to {target_language}. "
        f"Return ONLY a valid JSON array of objects, each with a 'text' key containing the translation "
        f"and an 'index' key matching the original segment index.\n\n"
    )
    for i, text in enumerate(segment_texts):
        prompt += f"[{i}] {text}\n"
    payload = {
        "model": config.translation_model,
        "messages": [
            {
                "role": "system",
                "content": "You are a professional translator. Return only valid JSON with no markdown formatting.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }
    response = call_openai_api("chat/completions", payload, config)
    result = TranslationResult.from_openai_response(
        response, target_language=target_language, source_language=source_lang
    )
    enriched_segments = []
    for i, seg in enumerate(segments):
        translated_text = seg.get("text", "")
        for translated_seg in result.segments:
            if translated_seg.get("index") == i:
                translated_text = translated_seg.get("text", translated_text)
                break
        enriched = dict(seg)
        enriched["translated_text"] = translated_text
        enriched["target_language"] = target_language
        enriched_segments.append(enriched)
    result.segments = enriched_segments
    return result


def translate_completed_transcript(
    job_id: str,
    target_language: str,
    source_language: Optional[str] = None,
    use_utterances: bool = True,
) -> TranslationResult:
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
    return translate_transcript_segments(
        segments, target_language, source_language=source_language
    )


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python translate_transcript.py <job_id> <target_language> [source_language]"
        )
        sys.exit(1)
    job_id = sys.argv[1]
    target_language = sys.argv[2]
    source_language = sys.argv[3] if len(sys.argv) > 3 else None
    result = translate_completed_transcript(
        job_id, target_language, source_language=source_language
    )
    output = {
        "source_language": result.source_language,
        "target_language": result.target_language,
        "translated_segments": result.segments,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
