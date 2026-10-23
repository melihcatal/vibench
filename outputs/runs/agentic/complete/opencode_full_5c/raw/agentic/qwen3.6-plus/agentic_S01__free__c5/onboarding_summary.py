import os
import logging
from typing import Optional, Dict, Any, List, Tuple

import openai

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

openai.api_key = OPENAI_API_KEY


def summarize_onboarding_state(
    user_id: str,
    onboarding_data: Dict[str, Any],
    model: Optional[str] = None,
) -> Tuple[Optional[str], Optional[str]]:
    target_model = model or OPENAI_MODEL

    data_summary_parts = []
    for key, value in onboarding_data.items():
        if isinstance(value, dict):
            sub_parts = [f"{k}: {v}" for k, v in value.items()]
            data_summary_parts.append(f"{key}: {', '.join(sub_parts)}")
        elif isinstance(value, list):
            data_summary_parts.append(f"{key}: {', '.join(str(v) for v in value)}")
        else:
            data_summary_parts.append(f"{key}: {value}")

    data_text = "\n".join(data_summary_parts)

    system_prompt = (
        "You are a support assistant. Summarize the following user onboarding state "
        "into a concise, clear summary that a support agent can quickly understand. "
        "Include account status, completed steps, pending actions, and any flags or issues. "
        "Keep the summary under 200 words."
    )

    try:
        response = openai.chat.completions.create(
            model=target_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"User ID: {user_id}\n\nOnboarding Data:\n{data_text}",
                },
            ],
            temperature=0.2,
            max_tokens=500,
        )

        summary = response.choices[0].message.content.strip()
        logger.info(
            "Generated onboarding summary for user %s using OpenAI %s",
            user_id,
            target_model,
        )
        return summary, None

    except openai.OpenAIError as exc:
        logger.error("OpenAI summarization failed for user %s: %s", user_id, exc)
        return None, str(exc)
