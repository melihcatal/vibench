from openai import OpenAI


def image_summary(labels, description, text):
    client = OpenAI()
    prompt = f"Labels: {labels}\nDescription: {description}\nText: {text}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
