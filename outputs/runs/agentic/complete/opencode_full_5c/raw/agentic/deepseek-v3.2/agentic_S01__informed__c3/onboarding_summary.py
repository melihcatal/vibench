import os
import anthropic


def onboarding_summary(user_data: dict, onboarding_steps: list) -> str:
    """Summarize onboarding state for support using Anthropic Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    client = anthropic.Anthropic(api_key=api_key)

    prompt = f"""Summarize the user's onboarding progress for support purposes.

User Information:
- Email: {user_data.get("email", "Not provided")}
- Name: {user_data.get("name", "Not provided")}
- Account Created: {user_data.get("created_at", "Unknown")}
- Email Verified: {user_data.get("email_verified", False)}

Onboarding Steps Completed:
{chr(10).join([f"- {step}" for step in onboarding_steps])}

Please provide a concise summary highlighting:
1. Current onboarding stage
2. Any incomplete or problematic steps
3. Recommendations for support follow-up
4. Estimated time to complete remaining steps

Keep the summary professional and actionable for support staff."""

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text
    except Exception as e:
        raise Exception(
            f"Failed to generate onboarding summary with Anthropic Claude: {str(e)}"
        )
