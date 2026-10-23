import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_json(text):
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=text, max_tokens=150
    )
    return response.choices[0].text.strip()
