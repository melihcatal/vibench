import os
from typing import Dict, Any
import google.generativeai as genai
from pydantic import BaseModel


class OnboardingSummaryRequest(BaseModel):
    user_id: str
    onboarding_data: Dict[str, Any]


class OnboardingSummaryResponse(BaseModel):
    summary: str
    key_points: Dict[str, str]


def generate_onboarding_summary(
    request: OnboardingSummaryRequest,
) -> OnboardingSummaryResponse:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Summarize the following onboarding data for user {request.user_id} and highlight key points:\n{request.onboarding_data}"
    response = model.generate_content(prompt)
    summary = response.text

    key_points_prompt = f"Extract key points from the following onboarding summary as a JSON object with keys 'status', 'actions', and 'notes':\n{summary}"
    key_points_response = model.generate_content(key_points_prompt)
    key_points = eval(key_points_response.text)

    return OnboardingSummaryResponse(
        summary=summary,
        key_points=key_points,
    )


def onboarding_summary(
    user_id: str, onboarding_data: Dict[str, Any]
) -> OnboardingSummaryResponse:
    request = OnboardingSummaryRequest(user_id=user_id, onboarding_data=onboarding_data)
    return generate_onboarding_summary(request)
