import os

from google.genai import Client


def onboarding_summary(onboarding_state: str):
    client = Client(api_key=os.environ["GOOGLE_API_KEY"])
    prompt = f"Summarize this onboarding state for support in one concise paragraph: {onboarding_state}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text
