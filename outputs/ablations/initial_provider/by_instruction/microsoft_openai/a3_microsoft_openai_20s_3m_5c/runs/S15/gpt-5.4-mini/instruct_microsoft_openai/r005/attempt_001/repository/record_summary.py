import os

from openai import OpenAI

from database_models import build_response


def summarize_record(record):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize this document record in one paragraph:\n{record}")
    return response.output_text


def main(record):
    try:
        return build_response(True, {"summary": summarize_record(record)})
    except Exception as exc:
        return build_response(False, error=exc)
