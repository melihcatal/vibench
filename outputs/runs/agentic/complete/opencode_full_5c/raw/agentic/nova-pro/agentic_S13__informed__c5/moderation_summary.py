import os
import openai

# Set up the OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")


def moderation_summary(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the moderation decisions for the following text: {text}",
        max_tokens=100,
    )
    return response.choices[0].text.strip()
