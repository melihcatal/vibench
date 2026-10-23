import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def stream_completion(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=prompt, max_tokens=150, stream=True
    )
    for part in response:
        yield part.choices[0].text.strip()
