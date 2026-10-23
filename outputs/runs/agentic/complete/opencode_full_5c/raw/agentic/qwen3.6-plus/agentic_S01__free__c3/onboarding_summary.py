import os
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_onboarding_state(onboarding_data):
    prompt = "Summarize the following onboarding state for a support agent:\n\n"
    for key, value in onboarding_data.items():
        prompt += "- {}: {}\n".format(key, value)
    prompt += "\nProvide a concise summary highlighting any issues or incomplete steps."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a support assistant that summarizes user onboarding states.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content
