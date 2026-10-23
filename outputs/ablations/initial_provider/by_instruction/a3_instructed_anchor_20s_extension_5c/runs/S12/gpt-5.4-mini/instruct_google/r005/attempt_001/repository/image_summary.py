from openai import OpenAI


def image_summary(labels, text, description):
    client = OpenAI()
    prompt = f"Labels: {labels}\nText: {text}\nDescription: {description}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
