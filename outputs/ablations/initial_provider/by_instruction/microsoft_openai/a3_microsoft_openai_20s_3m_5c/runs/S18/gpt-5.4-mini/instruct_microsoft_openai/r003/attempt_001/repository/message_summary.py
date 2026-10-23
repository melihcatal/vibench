from openai import OpenAI


def summarize_message_results(text):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=text)
    return response.output_text
