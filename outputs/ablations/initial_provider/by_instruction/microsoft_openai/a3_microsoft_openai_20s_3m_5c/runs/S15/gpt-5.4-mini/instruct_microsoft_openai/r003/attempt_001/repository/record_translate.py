from openai import OpenAI


def record_translate(record, target_language):
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate to {target_language}: {record}")
    return {"translation": response.output_text}
