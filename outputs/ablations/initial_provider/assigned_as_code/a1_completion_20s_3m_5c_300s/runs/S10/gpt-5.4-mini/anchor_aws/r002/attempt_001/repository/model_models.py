import json


def normalize_text_payload(payload):
    return {"text": payload["text"] if isinstance(payload, dict) else str(payload)}


def normalize_json_text(text):
    if isinstance(text, str):
        return json.loads(text)
    return text


def build_summary_prompt(text):
    return "Summarize the following text concisely:\n\n" + text


def build_extraction_prompt(text, schema):
    return "Extract JSON matching this schema:\n" + json.dumps(schema) + "\n\nText:\n" + text


def build_qa_prompt(question, context):
    return "Use the context to answer the question.\n\nContext:\n" + context + "\n\nQuestion:\n" + question
