from openai import OpenAI
from speech_client import get_openai_client
from speech_models import ModerationResult, TranscriptSegment


def moderate_transcript(segments: list[TranscriptSegment]) -> ModerationResult:
    client: OpenAI = get_openai_client()
    flagged_segments = []
    all_categories = {}
    all_scores = {}
    for idx, seg in enumerate(segments):
        response = client.moderations.create(
            input=seg.text, model="omni-moderation-latest"
        )
        result = response.results[0]
        if result.flagged:
            flagged_segments.append(idx)
        for cat, value in result.categories.model_dump().items():
            if value:
                all_categories[cat] = True
        for cat, score in result.category_scores.model_dump().items():
            all_scores[cat] = max(all_scores.get(cat, 0.0), score)
    return ModerationResult(
        flagged=len(flagged_segments) > 0,
        categories=all_categories,
        category_scores=all_scores,
        flagged_segments=flagged_segments,
    )


def moderate_text(text: str) -> ModerationResult:
    client: OpenAI = get_openai_client()
    response = client.moderations.create(input=text, model="omni-moderation-latest")
    result = response.results[0]
    categories = {
        cat: val for cat, val in result.categories.model_dump().items() if val
    }
    scores = result.category_scores.model_dump()
    return ModerationResult(
        flagged=result.flagged,
        categories=categories,
        category_scores=scores,
        flagged_segments=[0] if result.flagged else [],
    )
