import os
from openai import OpenAI
from typing import Dict, Any, List


def summarize_onboarding_state(
    user_data: Dict[str, Any], steps_completed: List[str], issues: List[str] = None
) -> Dict[str, Any]:
    """Summarize onboarding state for support using OpenAI GPT."""
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
        )

    client = OpenAI(api_key=api_key)

    # Prepare the prompt
    prompt = f"""Summarize the user onboarding state for support purposes.

User Information:
- User ID: {user_data.get("id", "N/A")}
- Email: {user_data.get("email", "N/A")}
- Display Name: {user_data.get("display_name", "N/A")}
- Account Created: {user_data.get("created_at", "N/A")}
- Email Verified: {user_data.get("email_verified", False)}

Onboarding Progress:
Steps Completed: {", ".join(steps_completed) if steps_completed else "None"}

Issues Encountered:
{chr(10).join(f"- {issue}" for issue in (issues or ["None"]))}

Please provide a concise summary that includes:
1. Overall onboarding status (percentage complete)
2. Key accomplishments
3. Current blockers or issues
4. Recommended next steps for support
5. Risk assessment (low/medium/high)

Format the response as a structured summary suitable for a support ticket."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful support assistant that summarizes user onboarding states for customer support teams.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        summary_text = response.choices[0].message.content

        # Estimate completion percentage
        total_steps = 5  # Typical onboarding steps: registration, email verification, profile setup, preferences, completion
        completed_count = len(steps_completed)
        completion_percentage = min(100, int((completed_count / total_steps) * 100))

        # Determine risk level based on issues
        risk_level = "low"
        if issues:
            if any(
                "critical" in issue.lower()
                or "failed" in issue.lower()
                or "error" in issue.lower()
                for issue in issues
            ):
                risk_level = "high"
            elif len(issues) > 2:
                risk_level = "medium"

        return {
            "user_id": user_data.get("id"),
            "email": user_data.get("email"),
            "onboarding_summary": summary_text,
            "completion_percentage": completion_percentage,
            "steps_completed": steps_completed,
            "steps_total": total_steps,
            "issues_count": len(issues or []),
            "risk_level": risk_level,
            "summary_generated_at": "now",  # In production, use datetime
            "provider": "openai",
            "model": "gpt-4",
            "support_ticket_ready": True,
        }

    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")


def generate_support_instructions(
    user_data: Dict[str, Any], specific_issue: str = None
) -> Dict[str, Any]:
    """Generate support instructions for a specific onboarding issue."""
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    prompt = f"""Generate support instructions for helping a user with onboarding.

User: {user_data.get("email", "Unknown")}
Issue: {specific_issue or "General onboarding assistance needed"}

Please provide:
1. Step-by-step troubleshooting instructions
2. Common solutions for this issue
3. When to escalate to engineering
4. Estimated resolution time
5. Customer communication tips

Format as clear, actionable instructions for a support agent."""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced customer support specialist providing clear troubleshooting instructions.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=400,
        )

        instructions = response.choices[0].message.content

        return {
            "user_id": user_data.get("id"),
            "issue": specific_issue or "general",
            "support_instructions": instructions,
            "provider": "openai",
            "model": "gpt-4",
            "escalation_needed": "escalate" in instructions.lower()
            or "engineering" in instructions.lower(),
        }

    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")
