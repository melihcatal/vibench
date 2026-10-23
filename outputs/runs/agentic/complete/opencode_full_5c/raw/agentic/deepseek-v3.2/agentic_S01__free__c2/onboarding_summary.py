import os
from openai import OpenAI
from typing import Dict, Any


def summarize_onboarding_state(user_data: Dict[str, Any]) -> str:
    """
    Summarize onboarding state for support using OpenAI's GPT model.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Summarize the following user onboarding data for support team review:
    
    User ID: {user_data.get("user_id", "N/A")}
    Email: {user_data.get("email", "N/A")}
    Registration Date: {user_data.get("registration_date", "N/A")}
    Profile Completion: {user_data.get("profile_completion", 0)}%
    Steps Completed: {user_data.get("steps_completed", [])}
    Issues Encountered: {user_data.get("issues", [])}
    Last Activity: {user_data.get("last_activity", "N/A")}
    
    Provide a concise summary highlighting:
    1. Overall onboarding progress
    2. Any blockers or issues
    3. Recommended next steps for support
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful support assistant that summarizes user onboarding data.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )

    return response.choices[0].message.content


def generate_support_ticket_summary(
    user_data: Dict[str, Any], issue_description: str
) -> Dict[str, Any]:
    """
    Generate a comprehensive support ticket summary for onboarding issues.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Create a support ticket summary for a user experiencing onboarding issues.
    
    User Data:
    - User ID: {user_data.get("user_id", "N/A")}
    - Email: {user_data.get("email", "N/A")}
    - Profile Completion: {user_data.get("profile_completion", 0)}%
    - Steps Completed: {user_data.get("steps_completed", [])}
    
    Issue Description: {issue_description}
    
    Generate a structured summary including:
    1. Issue categorization
    2. Severity level
    3. Recommended priority
    4. Suggested troubleshooting steps
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a technical support specialist creating structured ticket summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=400,
        temperature=0.2,
    )

    return {
        "summary": response.choices[0].message.content,
        "user_id": user_data.get("user_id"),
        "timestamp": user_data.get("last_activity"),
    }
