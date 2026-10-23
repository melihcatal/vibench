import os
from mistralai.client import MistralClient

os.environ["MISTRAL_API_KEY"] = "your-mistral-api-key"


def summarize_onboarding(text):
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    response = client.chat(
        model="mistral-tiny", messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content
