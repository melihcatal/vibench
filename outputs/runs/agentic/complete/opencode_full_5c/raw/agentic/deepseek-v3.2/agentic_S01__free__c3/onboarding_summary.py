import os
from typing import Dict, Any
from identity_models import UserProfile
from profile_moderation import check_profile_for_activation


def summarize_onboarding_state(
    user_profile: UserProfile, onboarding_steps: Dict[str, bool]
) -> Dict[str, Any]:
    """Summarize user onboarding state using OpenAI GPT for analysis."""
    import openai

    openai.api_key = os.environ.get("OPENAI_API_KEY")

    # Prepare onboarding data
    completed_steps = [
        step for step, completed in onboarding_steps.items() if completed
    ]
    pending_steps = [
        step for step, completed in onboarding_steps.items() if not completed
    ]

    # Check profile moderation
    moderation_check = check_profile_for_activation(user_profile)

    # Create summary prompt
    prompt = f"""
    User Profile:
    - Name: {user_profile.name or "Not provided"}
    - Email: {user_profile.email}
    - Locale: {user_profile.locale or "Not specified"}
    
    Onboarding Progress:
    - Completed steps: {", ".join(completed_steps) if completed_steps else "None"}
    - Pending steps: {", ".join(pending_steps) if pending_steps else "All completed"}
    
    Profile Moderation Status:
    - Overall safe: {moderation_check["overall_safe"]}
    - Issues: {", ".join(moderation_check["issues"]) if moderation_check["issues"] else "None"}
    
    Please provide a concise summary of this user's onboarding state for support purposes.
    Include:
    1. Overall completion percentage
    2. Key pending items
    3. Any red flags or concerns
    4. Recommended next actions for support
    """

    # Call OpenAI API
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful support assistant analyzing user onboarding data.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )

    summary_text = response.choices[0].message.content

    # Calculate completion percentage
    total_steps = len(onboarding_steps)
    completed_count = len(completed_steps)
    completion_percentage = (
        (completed_count / total_steps * 100) if total_steps > 0 else 0
    )

    return {
        "user_id": user_profile.user_id,
        "email": user_profile.email,
        "completion_percentage": round(completion_percentage, 1),
        "completed_steps": completed_steps,
        "pending_steps": pending_steps,
        "moderation_safe": moderation_check["overall_safe"],
        "moderation_issues": moderation_check["issues"],
        "ai_summary": summary_text,
        "recommended_actions": extract_recommendations(summary_text),
    }


def extract_recommendations(summary_text: str) -> list:
    """Extract actionable recommendations from AI summary."""
    recommendations = []
    lines = summary_text.split("\n")

    for line in lines:
        line_lower = line.lower()
        if any(
            keyword in line_lower
            for keyword in ["recommend", "suggest", "should", "need to", "action"]
        ):
            # Clean up the line
            clean_line = line.strip().lstrip("-•* ").strip()
            if clean_line and len(clean_line) > 10:  # Avoid very short lines
                recommendations.append(clean_line)

    return recommendations[:3]  # Return top 3 recommendations


def generate_support_ticket_summary(user_profile: UserProfile, issue: str) -> str:
    """Generate a support ticket summary using OpenAI."""
    import openai

    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"""
    User: {user_profile.name or "Unknown"} ({user_profile.email})
    Issue: {issue}
    
    Generate a concise support ticket summary that includes:
    1. User context
    2. Problem description
    3. Suggested priority level (Low/Medium/High)
    4. Initial troubleshooting steps
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a support ticket system generating helpful summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.2,
    )

    return response.choices[0].message.content
