from openai import OpenAI


def visual_safety_text(labels):
    client = OpenAI()
    prompt = f"Assess whether this visual label list contains unsafe text: {labels}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
