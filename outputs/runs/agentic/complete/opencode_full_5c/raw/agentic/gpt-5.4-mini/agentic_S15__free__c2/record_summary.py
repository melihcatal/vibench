from openai import OpenAI


def summarize_record(record):
    client = OpenAI()
    prompt = f"Summarize this document record in one concise sentence: {record}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return {"summary": response.output_text}
