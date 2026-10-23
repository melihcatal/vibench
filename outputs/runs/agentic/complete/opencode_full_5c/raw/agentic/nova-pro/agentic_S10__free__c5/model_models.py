from .model_client import get_headers, get_payload

import requests


def summarize_text(text):
    headers = get_headers()
    payload = get_payload(f"Summarize the following text: {text}", 100)
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    return response.json()["completion"]


def extract_json(text):
    headers = get_headers()
    payload = get_payload(f"Extract JSON from the following text: {text}", 100)
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    return response.json()["completion"]


def answer_with_context(question, context):
    headers = get_headers()
    payload = get_payload(
        f"Answer the following question using the provided context: {question}. Context: {context}",
        100,
    )
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=payload)
    return response.json()["completion"]


def stream_completion(text):
    headers = get_headers()
    payload = get_payload(text, 100)
    response = requests.post(
        ANTHROPIC_API_URL, headers=headers, json=payload, stream=True
    )
    for line in response.iter_lines():
        if line:
            print(line)
