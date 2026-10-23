import os
from openai import OpenAI
from identity_models import RegisterResponse

_openai_client = None

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client

def summarize_onboarding(user: RegisterResponse) -> str:
    client = get_openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize the onboarding state of this user for support."
            },
            {
                "role": "user",
                "content": f"User {user.display_name} ({user.email}) just registered."
            }
        ]
    )
    return response.choices[0].message.content