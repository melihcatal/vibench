import os
import json
from anthropic import Anthropic
from identity_models import SummaryRequest, SummaryResponse


def summarize_onboarding_state(user_id: str, onboarding_data: dict) -> SummaryResponse:
    """
    Summarize onboarding state for support using Anthropic Claude API.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY", "")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    # Prepare prompt for summarization
    prompt = f"""Summarize the onboarding state for user {user_id}.

Onboarding data:
{json.dumps(onboarding_data, indent=2)}

Please provide:
1. A brief summary of the user's onboarding progress
2. Completion percentage (0-100%)
3. Key next steps needed

Format the response as JSON with keys: summary, completion_percentage, next_steps."""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse the response
        content = response.content[0].text
        # Extract JSON from response
        import re

        json_match = re.search(r"\{.*\}", content, re.DOTALL)

        if json_match:
            result = json.loads(json_match.group())
        else:
            # Fallback parsing
            result = {
                "summary": content[:200],
                "completion_percentage": 50.0,
                "next_steps": ["Complete profile setup", "Verify email"],
            }

        return SummaryResponse(
            user_id=user_id,
            summary=result.get("summary", "Onboarding in progress"),
            completion_percentage=float(result.get("completion_percentage", 0.0)),
            next_steps=result.get("next_steps", []),
        )

    except Exception as e:
        # Fallback response
        return SummaryResponse(
            user_id=user_id,
            summary=f"Onboarding data available for user {user_id}. Error during AI summarization: {str(e)}",
            completion_percentage=0.0,
            next_steps=["Review onboarding data manually"],
        )
