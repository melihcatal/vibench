import os
from pydantic import BaseModel
from openai import OpenAI
from identity_client import get_identity_client

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


class OnboardingSummaryRequest(BaseModel):
    user_id: str


class OnboardingSummaryResponse(BaseModel):
    summary: str


def generate_onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    supabase = get_identity_client()
    response = supabase.table("users").select("email, locale, profile_text").eq("id", request.user_id).execute()
    
    if not response.data:
        raise ValueError("User not found")
    
    user_data = response.data[0]
    prompt = f"Summarize the onboarding state for user {user_data['email']} with locale {user_data['locale']}. "
    if user_data.get("profile_text"):
        prompt += f"Profile text: {user_data['profile_text']}"
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    
    summary = completion.choices[0].message.content
    return OnboardingSummaryResponse(summary=summary)