import os
from openai import OpenAI
from speech_models import TranscriptionResult


def archive_summary(
    transcript_result: TranscriptionResult,
    openai_api_key: str | None = None,
    model: str = "gpt-4o-mini",
    max_tokens: int = 500,
) -> dict:
    api_key = openai_api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    text = transcript_result.text
    if not text.strip():
        return {
            "transcription_id": transcript_result.transcription_id,
            "summary": "",
            "key_topics": [],
            "action_items": [],
            "participant_count": 0,
        }

    speakers = set()
    for utt in transcript_result.utterances:
        if utt.speaker:
            speakers.add(utt.speaker)

    system_prompt = (
        "You are an expert meeting summarizer. Analyze the provided meeting transcript "
        "and return a JSON object with the following keys: "
        "'summary' (a concise paragraph summary), "
        "'key_topics' (list of main discussion topics), "
        "'action_items' (list of action items or decisions made), "
        "'sentiment' (overall meeting sentiment: positive, neutral, or negative). "
        "Return only valid JSON."
    )

    user_prompt = f"Meeting transcript:\n\n{text}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    import json

    try:
        summary_data = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        summary_data = {
            "summary": response.choices[0].message.content,
            "key_topics": [],
            "action_items": [],
            "sentiment": "unknown",
        }

    return {
        "transcription_id": transcript_result.transcription_id,
        "summary": summary_data.get("summary", ""),
        "key_topics": summary_data.get("key_topics", []),
        "action_items": summary_data.get("action_items", []),
        "sentiment": summary_data.get("sentiment", "unknown"),
        "participant_count": len(speakers),
        "audio_duration_ms": transcript_result.audio_duration_ms,
        "model_used": model,
    }


if __name__ == "__main__":
    from speech_models import TranscriptionResult, TranscriptionStatus, UtteranceInfo

    sample = TranscriptionResult(
        transcription_id="test-789",
        status=TranscriptionStatus.COMPLETED,
        text="Welcome everyone. Today we discussed the Q4 roadmap. Action item: finalize budget by Friday.",
        utterances=[
            UtteranceInfo(
                text="Welcome everyone.", speaker="0", start_ms=0, end_ms=2000
            ),
            UtteranceInfo(
                text="Today we discussed the Q4 roadmap.",
                speaker="1",
                start_ms=2000,
                end_ms=6000,
            ),
        ],
    )
    result = archive_summary(sample)
    print(f"Summary: {result['summary']}")
