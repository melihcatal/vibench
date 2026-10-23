import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def answer_with_context(question, context):
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=f"{context} {question}", max_tokens=150
    )
    return response.choices[0].text.strip()
