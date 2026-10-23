import os
import openai

# Initialize the OpenAI API
openai.api_key = os.environ['OPENAI_API_KEY']

# Summarize onboarding state for support
def summarize_onboarding(text):
    try:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=text,
            max_tokens=150,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise e