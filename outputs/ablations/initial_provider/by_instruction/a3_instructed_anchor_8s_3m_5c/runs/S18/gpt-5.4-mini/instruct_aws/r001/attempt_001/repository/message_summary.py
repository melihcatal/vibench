from openai import OpenAI


def summarize_message(result):
    client = OpenAI()
    prompt = f"Summarize this message processing result in one sentence: {result}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
