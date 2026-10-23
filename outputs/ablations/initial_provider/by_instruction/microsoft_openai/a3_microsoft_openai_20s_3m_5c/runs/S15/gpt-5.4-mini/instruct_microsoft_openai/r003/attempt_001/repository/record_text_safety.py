from openai import OpenAI


def record_text_safety(record):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=str(record))
    return {"result": response.output_text}
