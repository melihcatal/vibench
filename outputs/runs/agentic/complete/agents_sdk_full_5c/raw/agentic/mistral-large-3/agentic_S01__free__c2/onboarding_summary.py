import os
from openai import OpenAI
from identity_models import RegisterUserResponse

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_onboarding_summary(user_data: dict) -> str:
    """Generate a summary of onboarding state using OpenAI GPT-3.5-turbo."""
    prompt = (
        f"Summarize the following onboarding data for support:"
        f"User ID: {user_data.get('user_id')}\n"
        f"Email: {user_data.get('email')}\n"
        f"Display Name: {user_data.get('display_name')}\n"
        f"Onboarding State: {user_data.get('onboarding_state')}\n"
        "Provide a concise summary for support agents."
    )
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()