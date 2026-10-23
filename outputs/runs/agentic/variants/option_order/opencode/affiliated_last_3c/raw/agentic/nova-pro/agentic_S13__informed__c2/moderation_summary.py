import os
import mistralai.client

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


def summarize_moderation(decisions):
    client = mistralai.client.Client(api_key=MISTRAL_API_KEY)
    prompt = f"Summarize the following moderation decisions: {decisions}"
    response = client.chat.completions.create(
        model="mistral-large-latest", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
