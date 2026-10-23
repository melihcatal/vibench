import os
import openai

def summarize_meeting(text):
    os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=150
    )
    return response.choices[0].text.strip()