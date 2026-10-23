import os
import json
from typing import Optional, Dict, Any, List

from openai import OpenAI


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_SUMMARY_MODEL = "gpt-4o-mini"

ONBOARDING_SUMMARY_PROMPT = """Summarize the following onboarding state for a support agent.
Include: user status, any flagged moderation items, translation locale, and recommended next actions.
Keep it concise and actionable.

Onboarding State:
{onboarding_state}"""


def get_client() -> OpenAI:
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    return OpenAI(api_key=api_key)


def summarize_onboarding_state(
    onboarding_data: Dict[str, Any],
    max_tokens: int = 500,
) -> Dict[str, Any]:
    client = get_client()

    state_json = json.dumps(onboarding_data, indent=2, default=str)
    prompt = ONBOARDING_SUMMARY_PROMPT.format(onboarding_state=state_json)

    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a support assistant that summarizes onboarding states for customer support agents.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary_text = response.choices[0].message.content

    return {
        "summary": summary_text,
        "model": OPENAI_SUMMARY_MODEL,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }


def generate_support_ticket_summary(
    user_id: str,
    onboarding_data: Dict[str, Any],
    issue_description: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_client()

    context = {
        "user_id": user_id,
        "onboarding_state": onboarding_data,
        "issue": issue_description,
    }
    context_json = json.dumps(context, indent=2, default=str)

    prompt = f"""Create a support ticket summary for this user.

Context:
{context_json}

Provide:
1. User overview
2. Onboarding progress
3. Identified issues or blockers
4. Recommended resolution steps"""

    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a support ticket assistant. Create clear, structured summaries for support agents.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=600,
        temperature=0.2,
    )

    return {
        "user_id": user_id,
        "ticket_summary": response.choices[0].message.content,
        "model": OPENAI_SUMMARY_MODEL,
        "issue_description": issue_description,
    }


def extract_onboarding_insights(
    batch_data: List[Dict[str, Any]],
) -> Dict[str, Any]:
    client = get_client()

    data_json = json.dumps(batch_data, indent=2, default=str)

    prompt = f"""Analyze this batch of onboarding states and provide insights:
- Common drop-off points
- Frequent moderation flags
- Locale distribution
- Recommended improvements

Data:
{data_json}"""

    response = client.chat.completions.create(
        model=OPENAI_SUMMARY_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an analytics assistant that identifies patterns in user onboarding data.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=800,
        temperature=0.4,
    )

    return {
        "batch_size": len(batch_data),
        "insights": response.choices[0].message.content,
        "model": OPENAI_SUMMARY_MODEL,
    }
