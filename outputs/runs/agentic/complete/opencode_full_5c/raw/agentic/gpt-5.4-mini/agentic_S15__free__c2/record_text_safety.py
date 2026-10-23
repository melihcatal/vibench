from openai import OpenAI


def check_record_text_safety(record):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Assess this document text for unsafe content and return a brief verdict: {record}",
    )
    return {"verdict": response.output_text}
