from openai import OpenAI


def visual_safety_text(labels):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Check these labels for unsafe text: {labels}")
    return response.output_text
