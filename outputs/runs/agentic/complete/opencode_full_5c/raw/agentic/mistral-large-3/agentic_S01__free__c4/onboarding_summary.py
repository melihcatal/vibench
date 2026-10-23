from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from identity_models import UserProfile
import os

# Initialize Mistral AI client with concrete model identifier
client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))


def onboarding_summary(profile: UserProfile) -> str:
    messages = [
        ChatMessage(
            role="system",
            content="You are a support assistant. Summarize the user's onboarding state concisely.",
        ),
        ChatMessage(
            role="user",
            content=f"User ID: {profile.user_id}, Email: {profile.email}, Onboarding Status: {profile.onboarding_status}",
        ),
    ]

    response = client.chat(model="mistral-large-latest", messages=messages)

    return response.choices[0].message.content
