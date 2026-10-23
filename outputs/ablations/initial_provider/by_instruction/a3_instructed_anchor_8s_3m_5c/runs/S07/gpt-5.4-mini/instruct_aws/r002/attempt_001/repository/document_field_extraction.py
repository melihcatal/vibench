from openai import OpenAI


def extract_document_fields(text: str) -> dict:
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Extract structured fields from:\n{text}")
    return response.model_dump()
