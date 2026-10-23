import os
import json
from openai import OpenAI
from safety_models import ModerationResponse, BatchModerationResponse


def get_openai_client() -> OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key)


def summarize_moderation_decision(
    moderation_result: ModerationResponse,
    model: str = "gpt-4o-mini",
    client: OpenAI | None = None,
) -> str:
    if client is None:
        client = get_openai_client()

    violations = moderation_result.violating_categories
    scores_summary = "\n".join(
        f"- {s.category}: {s.score:.4f} (threshold: {s.threshold})"
        for s in moderation_result.scores
    )

    prompt = (
        f"Summarize this content moderation decision in 2-3 sentences.\n\n"
        f"Text analyzed: {moderation_result.text[:500]}\n"
        f"Overall violation: {moderation_result.overall_violation}\n"
        f"Violating categories: {', '.join(violations) if violations else 'None'}\n"
        f"Scores:\n{scores_summary}\n\n"
        f"Provide a concise summary suitable for a moderation review log."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation summarizer. Provide clear, factual summaries of moderation decisions.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=200,
    )

    return response.choices[0].message.content.strip()


def summarize_batch_moderation(
    batch_result: BatchModerationResponse,
    model: str = "gpt-4o-mini",
    client: OpenAI | None = None,
) -> str:
    if client is None:
        client = get_openai_client()

    flagged_items = []
    for r in batch_result.results:
        if r.overall_violation:
            flagged_items.append(
                {
                    "text": r.text[:200],
                    "violating_categories": r.violating_categories,
                    "max_score": r.max_score,
                    "max_category": r.max_category,
                }
            )

    summary_input = json.dumps(
        {
            "total_messages": batch_result.total_messages,
            "flagged_count": batch_result.flagged_count,
            "clean_count": batch_result.clean_count,
            "flagged_items": flagged_items[:20],
        },
        indent=2,
    )

    prompt = (
        f"Summarize this batch moderation report in 3-5 sentences.\n\n"
        f"Batch moderation summary:\n{summary_input}\n\n"
        f"Provide a concise executive summary suitable for a moderation team lead."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation analyst. Provide clear, data-driven summaries of batch moderation results.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=300,
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    from moderate_text import moderate_text

    input_text = "This is a test message for moderation."
    result = moderate_text(input_text)
    summary = summarize_moderation_decision(result)
    print(f"Summary: {summary}")
