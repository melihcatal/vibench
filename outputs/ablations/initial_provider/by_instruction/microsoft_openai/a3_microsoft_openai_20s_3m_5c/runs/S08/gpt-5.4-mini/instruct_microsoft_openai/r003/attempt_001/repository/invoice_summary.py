from openai import OpenAI


def invoice_summary(extracted):
    client = OpenAI(api_key=None)
    return client.responses.create(model="gpt-5.4-mini", input=str(extracted)).output_text
