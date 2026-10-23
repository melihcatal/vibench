import os
from openai import OpenAI
from identity_models import RegisterUserResponse

# Initialize OpenAI client with provider-specific model
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_onboarding(user: RegisterUserResponse, notes: str) -> str:
    prompt = (
        f"Summarize the following onboarding details for support:"
        f"User ID: {user.user_id}\n"
        f"Notes: {notes}\n"
        f"Provide a concise summary for support agents."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Use a concrete model identifier
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    return response.choices[0].message.content.strip()