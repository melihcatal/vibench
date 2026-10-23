from openai import OpenAI


def record_summary(record, model="gpt-5.4-mini"):
    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=f"Summarize this document record concisely: {record}",
    )
    return response.output_text
