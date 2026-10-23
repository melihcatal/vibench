import os
import mistralai

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def summarize_moderation_decisions(decisions):
    client = mistralai.Client(api_key=MISTRAL_API_KEY)
    response = client.create_completion(
        model="mistral-medium",
        prompt=f"Summarize the following moderation decisions: {decisions}",
        max_tokens=150,
    )
    return response.choices[0].text.strip()
