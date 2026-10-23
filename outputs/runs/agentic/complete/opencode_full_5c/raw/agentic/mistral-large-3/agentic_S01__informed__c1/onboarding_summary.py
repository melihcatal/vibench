from typing import Dict, Any
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse

# Initialize Mistral AI client with provider-specific credentials
mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    """
    Summarizes onboarding state for support using Mistral's chat API.
    """
    try:
        messages = [
            ChatMessage(
                role="system",
                content="You are a support assistant. Summarize the user's onboarding state concisely.",
            ),
            ChatMessage(
                role="user",
                content=f"User ID: {request.user_id}. Onboarding steps completed: {request.steps_completed}. "
                f"Additional context: {request.context}",
            ),
        ]

        response = mistral_client.chat(model="mistral-large-latest", messages=messages)

        return OnboardingSummaryResponse(
            success=True, summary=response.choices[0].message.content
        )
    except Exception as e:
        return OnboardingSummaryResponse(success=False, error=str(e))
