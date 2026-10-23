from openai import OpenAI


def metric_annotation_safety(text: str):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Assess whether the following metric annotation is unsafe. Return a brief JSON object with safe and reason fields: {text}")
    return response.output_text
