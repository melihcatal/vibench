import json
from safety_client import get_openai_client, CHAT_MODEL
from safety_models import BatchModerationResult, ModerationResult


SUMMARY_SYSTEM_PROMPT = """You are a content moderation analyst. Summarize moderation decisions clearly and concisely.
Focus on: overall safety posture, most common violation categories, severity patterns, and recommended actions.
Keep the summary under 200 words."""


def summarize_moderation_decisions(results: BatchModerationResult) -> str:
    decision_data = []
    for r in results.results:
        flagged_cats = [c.category for c in r.categories if c.flagged]
        decision_data.append(
            {
                "text_preview": r.text[:100],
                "flagged": r.flagged,
                "categories": flagged_cats,
                "highest_score": r.highest_score,
            }
        )

    analysis_input = json.dumps(decision_data, indent=2)
    user_prompt = f"Summarize these moderation decisions:\n{analysis_input}"

    client = get_openai_client()
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


def generate_flagged_summary(results: BatchModerationResult) -> str:
    flagged_results = [r for r in results.results if r.flagged]
    if not flagged_results:
        return "No content was flagged in this batch."

    decision_data = []
    for r in flagged_results:
        flagged_cats = [c.category for c in r.categories if c.flagged]
        decision_data.append(
            {
                "text_preview": r.text[:100],
                "categories": flagged_cats,
                "highest_score": r.highest_score,
            }
        )

    analysis_input = json.dumps(decision_data, indent=2)
    user_prompt = f"Summarize these flagged moderation decisions:\n{analysis_input}"

    client = get_openai_client()
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


def summarize_single_decision(result: ModerationResult) -> str:
    flagged_cats = [c.category for c in result.categories if c.flagged]
    decision_data = {
        "text_preview": result.text[:200],
        "flagged": result.flagged,
        "categories": flagged_cats,
        "highest_score": result.highest_score,
    }

    analysis_input = json.dumps(decision_data, indent=2)
    user_prompt = f"Summarize this moderation decision:\n{analysis_input}"

    client = get_openai_client()
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content
