import os
import openai
from typing import Dict, Any


def onboarding_summary(onboarding_data: Dict[str, Any]) -> str:
    """Summarize onboarding state for support using OpenAI GPT."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    openai.api_key = api_key

    prompt = f"""
    Summarize the following user onboarding data for customer support:
    
    User Information:
    - Email: {onboarding_data.get("email", "Not provided")}
    - Name: {onboarding_data.get("name", "Not provided")}
    - Account Created: {onboarding_data.get("created_at", "Unknown")}
    - Email Verified: {onboarding_data.get("email_verified", False)}
    
    Onboarding Steps Completed:
    {onboarding_data.get("completed_steps", [])}
    
    Profile Information:
    {onboarding_data.get("profile_data", {})}
    
    Issues or Notes:
    {onboarding_data.get("issues", [])}
    
    Please provide a concise summary highlighting:
    1. Basic user information
    2. Onboarding progress
    3. Any issues or concerns
    4. Recommended next steps for support
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful customer support assistant that summarizes user onboarding data.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        raise Exception(f"OpenAI GPT summarization failed: {str(e)}")
