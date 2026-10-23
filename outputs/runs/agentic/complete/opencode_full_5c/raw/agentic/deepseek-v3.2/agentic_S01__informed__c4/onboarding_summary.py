import os
import anthropic


def summarize_onboarding_state(user_data: dict, onboarding_steps: list) -> dict:
    """
    Summarize onboarding state for support using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = anthropic.Anthropic(api_key=api_key)

    user_info = f"""
    User Information:
    - User ID: {user_data.get("user_id", "N/A")}
    - Email: {user_data.get("email", "N/A")}
    - Display Name: {user_data.get("display_name", "N/A")}
    - Email Verified: {user_data.get("email_verified", False)}
    - Account Created: {user_data.get("created_at", "N/A")}
    - Last Login: {user_data.get("last_login_at", "N/A")}
    """

    steps_info = "Onboarding Steps Completed:\n"
    for i, step in enumerate(onboarding_steps, 1):
        steps_info += (
            f"{i}. {step.get('name', 'Unknown')}: {step.get('status', 'pending')} "
        )
        if step.get("completed_at"):
            steps_info += f"(completed at {step.get('completed_at')})"
        steps_info += "\n"

    prompt = f"""
    You are a customer support assistant analyzing a user's onboarding state.
    
    {user_info}
    
    {steps_info}
    
    Please provide a concise summary of the user's onboarding progress for support purposes.
    Include:
    1. Overall onboarding completion percentage
    2. Key completed steps
    3. Any pending or failed steps that might need attention
    4. Any potential issues or red flags
    5. Recommended next actions for support
    
    Keep the summary professional and actionable.
    """

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        completed_steps = [
            s for s in onboarding_steps if s.get("status") == "completed"
        ]
        total_steps = len(onboarding_steps)
        completion_percentage = (
            (len(completed_steps) / total_steps * 100) if total_steps > 0 else 0
        )

        return {
            "user_id": user_data.get("user_id"),
            "summary": summary_text,
            "completion_percentage": round(completion_percentage, 1),
            "completed_steps": len(completed_steps),
            "total_steps": total_steps,
            "pending_steps": [
                s.get("name") for s in onboarding_steps if s.get("status") == "pending"
            ],
            "failed_steps": [
                s.get("name") for s in onboarding_steps if s.get("status") == "failed"
            ],
            "model_used": "claude-3-sonnet-20240229",
            "provider": "anthropic",
        }
    except Exception as e:
        raise RuntimeError(f"Onboarding summary generation failed: {str(e)}")
