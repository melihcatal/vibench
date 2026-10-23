import json

from openai import OpenAI


client = OpenAI()


def summarize_record(record):
    prompt = f"Summarize this document in one short sentence:\n{json.dumps(record, ensure_ascii=False)}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text


def handler(event, context=None):
    return {"statusCode": 200, "body": json.dumps({"ok": True, "summary": summarize_record(event)})}
