from openai import OpenAI


def record_summary(record):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=str(record))
    return {"summary": response.output_text}
