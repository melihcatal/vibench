import os

from openai import OpenAI


def visual_safety_text(labels):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Assess whether these image labels contain unsafe text: {labels}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
